from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Ism", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Familiya", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email manzil", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Foydalanuvchi nomi", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Parol", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
