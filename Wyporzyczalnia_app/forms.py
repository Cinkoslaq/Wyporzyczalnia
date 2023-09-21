from django import forms

from Wyporzyczalnia_app.models import Machinery, Comments, Company, Ratings


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Podaj nazwę użytkownika", max_length=64)
    password = forms.CharField(label="Podaj haslo", max_length= 64, widget=forms.PasswordInput())

class AddUserForm(forms.Form):
    login = forms.CharField(label="Login")
    password = forms.CharField(label="Podaj haslo", max_length=64, widget=forms.PasswordInput())
    rep_pass = forms.CharField(label="Podaj haslo", max_length=64, widget=forms.PasswordInput())
    name = forms.CharField(label="Imię")
    lastname = forms.CharField(label="Nazwisko")
    mail = forms.CharField(label="Email", max_length=64, widget=forms.EmailInput())


class AddMachineryForm(forms.ModelForm):
    comment = forms.CharField(
        label="Dodaj komentarz",
        widget=forms.Textarea(attrs={'cols': 40, 'rows': 5})
    )

    # Pole dostawy
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

    class Meta:
        model = Machinery
        fields = ['name', 'categories', 'rental_price_per_day', 'comment']


class AddCompanyForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nazwa użytkownika")
    nip = forms.CharField(max_length=15, label="NIP")
    address = forms.CharField(max_length=200, label="Adres")
    description = forms.CharField(widget=forms.Textarea, label="Opis")

class AddCommentForm(forms.ModelForm):
    content = forms.CharField(
        label="Dodaj komentarz",
        widget=forms.Textarea(attrs={'cols': 40, 'rows': 5})
    )

    # Dodaj pole do wyboru firmy
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),  # To pobierze wszystkie dostępne firmy z bazy danych
        label="Wybierz firmę"
    )

    class Meta:
        model = Comments
        fields = ['company', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

class AddRatingForm(forms.ModelForm):
    class Meta:
        model = Ratings
        fields = ['rating']