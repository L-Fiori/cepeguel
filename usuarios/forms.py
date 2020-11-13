from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from usuarios.models import Usuario

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Obrigatório. Insira um endereço de email válido.')

    class Meta:
        model = Usuario
        fields = ('email', 'telephone', 'nusp', 'first_name', 'last_name', 'password1', 'password2')

class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")