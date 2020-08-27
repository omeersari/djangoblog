from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Kullanıcı Adı giriniz')
    email = forms.EmailField(label='Email', max_length=60, help_text='Gerekli, lütfen geçerli bir email adresi giriniz')
    password1 = forms.CharField(label='Şifre')
    password2 = forms.CharField(label='Şifre Doğrula')

    class Meta:
        model = Account
        fields = ('email', 'username')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Şifre', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Şifre veya Email adresi hatalı")
