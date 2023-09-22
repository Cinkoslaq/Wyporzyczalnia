from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required


from .models import Machinery, Rental, Company, Ratings, Comments, Category, Delivery
from .forms import AddUserForm, LoginUserForm, AddMachineryForm, CommentForm, AddCommentForm


def home(request):
    """Widok strony głównej - strona główna."""
    return render(request, 'home.html')


def uslugi(request):
    """Widok strony usług - przedstawienie usług."""
    opis_uslug = "Główne usługi naszego portalu to wypożyczanie maszyn budowlanych, rolniczych oraz transportu w razie przeprowadzki. Nie kupuj, lepiej wypożycz!"
    return render(request, 'uslugi.html', {'opis_uslug': opis_uslug})


def onas(request):
    """Widok strony o tworcach aplikacji."""
    komunikat = "Witamy, jesteśmy nowi na rynku i stworzyliśmy tę aplikację głównie do wypożyczania, aby nie kupować i nie przepłacać."
    return render(request, 'onas.html', {'komunikat': komunikat})


def machinery_list(request):
    """Widok listy maszyn."""
    machinery_items = Machinery.objects.all()
    return render(request, 'machinery_list.html', {'machinery_items': machinery_items})


def machinery_detail_view(request, machinery_id):
    """Widok szczegółów maszyny."""
    # Pobierz maszynę o określonym identyfikatorze lub zwróć 404, jeśli nie istnieje.
    machinery = get_object_or_404(Machinery, pk=machinery_id)
    # Pobierz wszystkie komentarze przypisane do tej maszyny.
    comments = machinery.comments.all()
    # Przygotuj dane do przekazania do szablonu 'machinery_detail.html'.
    # Wyrenderuj szablon z danymi i zwróć jako odpowiedź.
    return render(request, 'machinery_detail.html', {'machinery': machinery, 'comments': comments})


def rental_list(request):
    """Widok listy wynajmów."""
    # Pobierz wszystkie obiekty typu Rental z bazy danych.
    rental_items = Rental.objects.all()
    # Przygotuj dane do przekazania do szablonu 'rental_list.html'.
    # Wyrenderuj szablon z danymi i zwróć jako odpowiedź.
    return render(request, 'rental_list.html', {'rental_items': rental_items})


def rental_detail(request, rental_id):
    """Widok szczegółów wynajmu."""
    # Pobierz obiekt typu Rental o podanym identyfikatorze (pk) lub wyświetl stronę 404, jeśli obiekt nie istnieje.
    rental = get_object_or_404(Rental, pk=rental_id)
    # Przygotuj dane do przekazania do szablonu 'rental_detail.html'.
    # Wyrenderuj szablon z danymi i zwróć jako odpowiedź.
    return render(request, 'rental_detail.html', {'rental': rental})


def company_detail(request, company_id):
    """Widok szczegółów firmy."""
    # Pobierz obiekt firmy o podanym identyfikatorze (pk) lub wyświetl stronę 404, jeśli obiekt nie istnieje.
    company = get_object_or_404(Company, pk=company_id)
    # Pobierz oceny wystawione dla tej firmy.
    ratings = Ratings.objects.filter(company=company)
    # Pobierz komentarze dotyczące firmy.
    comments = Comments.objects.filter(company=company)
    # Przygotuj dane do przekazania do szablonu 'company_detail.html'.
    # Wyrenderuj szablon z danymi i zwróć jako odpowiedź.
    return render(request, 'company_detail.html', {'company': company, 'ratings': ratings, 'comments': comments})


def add_rating(request, company_id):
    """Widok dodawania oceny dla firmy."""
    if request.method == 'POST':
        # Sprawdź, czy formularz został przesłany metodą POST.
        rating_value = request.POST['rating'] # Pobierz wartość oceny z formularza.
        company = get_object_or_404(Company, pk=company_id) # Pobierz obiekt firmy o podanym identyfikatorze (pk) lub wyświetl stronę 404, jeśli firma nie istnieje.
        # Utwórz nowy obiekt Ratings, który reprezentuje ocenę dla danej firmy.
        Ratings.objects.create(company=company, rating=rating_value)
        # Po dodaniu oceny, przekieruj użytkownika z powrotem do widoku szczegółów firmy.
        return HttpResponseRedirect(reverse('company_detail', args=(company_id,)))
    else:
        # Jeśli metoda żądania nie jest POST, wyrenderuj stronę dodawania oceny.
        return render(request, 'add_rating.html')


@login_required  # Dodaj dekorator login_required
def add_comment(request, machinery_id):
    """Widok dodawania komentarza dla maszyny."""
    # Pobierz obiekt maszyny o podanym identyfikatorze (pk) lub wyświetl stronę 404, jeśli maszyna nie istnieje.
    machinery = get_object_or_404(Machinery, pk=machinery_id)

    if request.method == 'POST':
        # Sprawdź, czy formularz został przesłany metodą POST.
        form = AddCommentForm(request.POST)
        if form.is_valid():
            # Jeśli formularz jest prawidłowy, pobierz treść komentarza z formularza.
            content = form.cleaned_data['content']
            # Pobierz lub utwórz instancję Company dla zalogowanego użytkownika.
            company, created = Company.objects.get_or_create(user=request.user)
            # Utwórz nowy obiekt Comments, który reprezentuje komentarz dla danej firmy.
            comment = Comments.objects.create(company=company, content=content)
            # Dodaj komentarz do maszyny.
            machinery.comments.add(comment)
            # Po dodaniu komentarza, przekieruj użytkownika z powrotem do widoku szczegółów maszyny.
            return redirect('machinery_detail', machinery_id=machinery_id)
    else:
        # Jeśli metoda żądania nie jest POST, wyświetl formularz do dodawania komentarza.
        form = AddCommentForm()
    # Wyrenderuj stronę z formularzem.
    return render(request, 'add_comment.html', {'form': form})


def add_machinery(request):
    """Widok dodawania maszyny."""
    if request.method == 'POST':
        # Sprawdź, czy żądanie jest przesyłane za pomocą metody POST.
        form = AddMachineryForm(request.POST)
        if form.is_valid():
            # Jeśli formularz jest prawidłowy, zapisz dane z formularza jako nową instancję maszyny.
            machinery = form.save()
            # Po zapisaniu maszyny, przekieruj użytkownika do widoku szczegółów tej maszyny.
            return redirect('machinery_detail', machinery_id=machinery.id)
    else:
        # Jeśli metoda żądania nie jest POST, wyświetl pusty formularz dodawania maszyny.
        form = AddMachineryForm()
    # Wyrenderuj stronę z formularzem.
    return render(request, 'add_machinery.html', {'form': form})


class LoginUser(View):
    """Widok logowania użytkownika."""
    def get(self, request):
        # Obsłuż żądanie typu GET, czyli wyświetlenie formularza logowania.
        form = LoginUserForm()
        return render(request, 'login_user.html', {'form': form})

    def post(self, request):
        # Obsłuż żądanie typu POST, czyli przesłanie danych logowania przez użytkownika.
        form = LoginUserForm(request.POST)
        if form.is_valid():
            # Jeśli formularz jest prawidłowy, pobierz nazwę użytkownika i hasło.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Autentykacja użytkownika za pomocą funkcji authenticate.
            user = authenticate(username=username, password=password)
            if user is not None:
                # Jeśli użytkownik został zautentykowany, zaloguj go.
                login(request, user)
                message = 'Udało się zalogować' + request.user.username
                ctx = {
                    'message': message,
                    'form': form,
                }
                # Wyrenderuj stronę informującą o udanym logowaniu.
                return render(request, 'login_user.html', context=ctx)
            else:
                # Jeśli użytkownik nie został zautentykowany, wyświetl komunikat o błędnych danych logowania.
                message = 'Nie udało się zalogować! :('
                ctx = {
                    'message': message,
                    'form': form,
                }
                # Wyrenderuj stronę z informacją o nieudanym logowaniu.
                return render(request, 'login_user.html', context=ctx)


class LogoutUser(View):
    """Widok wylogowania użytkownika."""
    def get(self, request):
        # Wyloguj użytkownika za pomocą funkcji logout.
        logout(request)
        # Przygotuj komunikat informujący o wylogowaniu.
        message = 'Użytkownik wylogowany, zaloguj ponownie!'
        ctx = {
            'message': message,
        }
        # Wyrenderuj stronę informującą o wylogowaniu.
        return render(request, 'logout_user.html', context=ctx)


class AddUser(View):
    """Widok rejestracji użytkownika."""
    def get(self, request):
        # Tworzenie formularza do rejestracji użytkownika.
        form = AddUserForm()
        # Wyrenderowanie strony rejestracji z pustym formularzem.
        return render(request, 'add_user.html', {'form': form})

    def post(self, request):
        # Tworzenie formularza na podstawie danych przesłanych w żądaniu POST.
        form = AddUserForm(request.POST)
        # Sprawdzenie, czy formularz jest poprawny.
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            rep_password = form.cleaned_data['rep_pass']
            name = form.cleaned_data['name']
            lastname = form.cleaned_data['lastname']
            mail = form.cleaned_data['mail']
            # Sprawdzenie, czy istnieje użytkownik o takim samym loginie.
            try:
                user = User.objects.get(username=login)
            except User.DoesNotExist:
                user = None
            # Jeśli użytkownik o podanym loginie już istnieje, wyświetl komunikat.
            if user is not None:
                mass = 'Login użytkownika istnieje spróbuj ponownie'
                ctx = {
                    'message': mass,
                    'form': form,
                }
                return render(request, 'add_user.html', context=ctx)
            else:
                if password == rep_password:
                    # Jeśli hasło i powtórzone hasło są zgodne, utwórz nowego użytkownika.
                    user_stop = User.objects.create_user(username=login, first_name=name, last_name=lastname,
                                                         email=mail, password=password)
                    mass = 'Użytkownik ' + login + ' został dodany!.'
                    ctx = {
                        'message': mass,
                        'form': form,
                    }
                    return render(request, 'add_user.html', context=ctx)
                else:
                    # Jeśli hasła się nie zgadzają, wyświetl odpowiedni komunikat.
                    mass = 'Hasło się nie zgadza!'
                    ctx = {
                        'message': mass,
                        'form': form,
                    }
                    return render(request, 'add_user.html', context=ctx)


def add_company(request):
    """Widok do dodawania nowej firmy."""
    # Sprawdzenie, czy żądanie jest typu POST (czy formularz został zatwierdzony).
    if request.method == 'POST':
        # Pobranie danych z formularza, które zostały przesłane za pomocą żądania POST.
        username = request.POST['username']
        nip = request.POST['nip']
        address = request.POST['address']
        description = request.POST['description']
        # Pobranie lub utworzenie instancji użytkownika na podstawie podanej nazwy użytkownika.
        user, created = User.objects.get_or_create(username=username)
        # Utworzenie nowej instancji firmy z przekazanymi danymi.
        company = Company.objects.create(user=user, NIP=nip, address=address, description=description)
        # Przekierowanie użytkownika do strony szczegółów firmy.
        return HttpResponseRedirect(reverse('company_detail', args=(company.id,)))
    else:
        # Jeśli żądanie jest typu GET, wyświetl formularz do dodawania firmy.
        return render(request, 'add_company.html')


def add_delivery(request, rental_id):
    if request.method == 'POST':
        delivery_type = request.POST.get('delivery_type')
        rental = get_object_or_404(Rental, pk=rental_id)
        Delivery.objects.create(rental=rental, delivery_type=delivery_type)

        # Przekieruj na URL lub nazwę widoku, a nie na nazwę pliku HTML
        return redirect('machinery_list')  # Użyj odpowiedniej nazwy widoku

    return render(request, 'add_delivery.html')
def company_list(request):
    """Widok listy firm."""
    # Pobranie wszystkich firm z bazy danych za pomocą zapytania do modelu Company.
    companies = Company.objects.all()
    # Przygotowanie kontekstu, czyli danych, które zostaną przekazane do szablonu 'company_list.html'.
    # Wyrenderowanie szablonu 'company_list.html' z przekazanymi danymi i zwrócenie jako odpowiedź.
    return render(request, 'company_list.html', {'companies': companies})

def delete_machinery(request, machinery_id):
    """Widok do usuwania maszyny."""
    # Pobranie maszyny o określonym identyfikatorze (machinery_id) lub wyświetlenie strony 404, jeśli maszyna nie istnieje.
    machinery = get_object_or_404(Machinery, pk=machinery_id)

    if request.method == 'POST':
        # Jeśli metoda żądania to POST (czyli formularz został przesłany), to usuwamy maszynę z bazy danych.
        machinery.delete()
        return redirect('machinery_list')  # Przekieruj na listę maszyn lub inny widok po usunięciu
    # Jeśli metoda żądania to GET (czyli użytkownik otworzył stronę bez przesłania formularza), to wyświetlamy stronę potwierdzenia usunięcia.
    return render(request, 'delete_machinery.html', {'machinery': machinery})


