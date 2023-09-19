from django import forms

from Wyporzyczalnia_app.models import Machinery


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
    class Meta:
        model = Machinery
        fields = ['name', 'categories', 'rental_price_per_day']

