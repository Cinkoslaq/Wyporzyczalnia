from django import forms

from Wyporzyczalnia_app.models import Machinery, Comments, Company, Ratings


class LoginUserForm(forms.Form):
    """Formularz logowania użytkownika."""
    # Pole do wprowadzenia nazwy użytkownika.
    username = forms.CharField(label="Podaj nazwę użytkownika", max_length=64)
    # Pole do wprowadzenia hasła, z użyciem widgetu PasswordInput, który ukrywa wprowadzone hasło.
    password = forms.CharField(label="Podaj haslo", max_length= 64, widget=forms.PasswordInput())

class AddUserForm(forms.Form):
    """Formularz do rejestracji nowego użytkownika."""
    # Pole do wprowadzenia loginu użytkownika.
    login = forms.CharField(label="Login")
    # Pole do wprowadzenia hasła, z użyciem widgetu PasswordInput, który ukrywa wprowadzone hasło.
    password = forms.CharField(label="Podaj haslo", max_length=64, widget=forms.PasswordInput())
    # Pole do ponownego wprowadzenia hasła w celu potwierdzenia.
    rep_pass = forms.CharField(label="Podaj haslo", max_length=64, widget=forms.PasswordInput())
    # Pole do wprowadzenia imienia użytkownika.
    name = forms.CharField(label="Imię")
    # Pole do wprowadzenia nazwiska użytkownika.
    lastname = forms.CharField(label="Nazwisko")
    # Pole do wprowadzenia adresu e-mail użytkownika.
    mail = forms.CharField(label="Email", max_length=64, widget=forms.EmailInput())


class AddMachineryForm(forms.ModelForm):
    """Formularz dodawania maszyny do wypożyczalni."""
    # Pole do dodawania komentarza z użyciem wielowierszowego pola tekstowego.
    comment = forms.CharField(
        label="Dodaj komentarz",
        widget=forms.Textarea(attrs={'cols': 40, 'rows': 5})
    )

    # Pole do wyboru rodzaju dostawy maszyny, wykorzystujące wybór typu radiowego - co oznacza wybranie tylko jednej opcji dostawy.
    DELIVERY_CHOICES = [
        ('self-pickup', 'Self Pickup'),
        ('express-delivery', 'Express Delivery'),
        ('standard-delivery', 'Standard Delivery'),
    ]
    delivery_type = forms.ChoiceField(
        label="Wybierz rodzaj dostawy",
        choices=DELIVERY_CHOICES,
        widget=forms.RadioSelect,
    )

    # Klasa Meta informuje formularz o tym, z którego modelu ma być utworzony i które pola modelu mają być uwzględnione w formularzu.
    class Meta:
        model = Machinery # Model, na podstawie którego tworzony jest formularz.
        fields = ['name', 'categories', 'rental_price_per_day', 'comment'] # Pola modelu, które mają być uwzględnione w formularzu.


class AddCompanyForm(forms.Form):
    """Formularz dodawania nowej firmy."""
    # Pole do wprowadzenia nazwy użytkownika firmy.
    username = forms.CharField(max_length=100, label="Nazwa użytkownika")
    # Pole do wprowadzenia numeru NIP firmy.
    nip = forms.CharField(max_length=15, label="NIP")
    # Pole do wprowadzenia adresu firmy.
    address = forms.CharField(max_length=200, label="Adres")
    # Pole do wprowadzenia opisu firmy, korzystające z widgetu Textarea.
    description = forms.CharField(widget=forms.Textarea, label="Opis")

class AddCommentForm(forms.ModelForm):
    """Formularz dodawania komentarza."""

    # Pole tekstowe do wprowadzenia treści komentarza.
    content = forms.CharField(
        label="Dodaj komentarz",
        widget=forms.Textarea(attrs={'cols': 40, 'rows': 5})
    )

    # Pole do wyboru firmy, z którym jest związany komentarz.
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),  # To pobierze wszystkie dostępne firmy z bazy danych
        label="Wybierz firmę"
    )

    class Meta:
        model = Comments
        fields = ['company', 'content']

class CommentForm(forms.ModelForm):
    """Formularz komentarza."""
    class Meta:
        model = Comments
        fields = ['content']

class AddRatingForm(forms.ModelForm):
    """Formularz dodawania oceny."""
    class Meta:
        model = Ratings
        fields = ['rating']
