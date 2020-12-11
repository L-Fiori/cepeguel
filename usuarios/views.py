from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from usuarios.forms import RegistrationForm, AccountAuthenticationForm

from .models import Usuario

def registration_view(request):
    '''
    Possibilita que as informações do cadastro sejam conferidas e, caso estejam válidas,
    sejam armazenadas no banco de dados.
    '''

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            usuario = authenticate(email=email, password=raw_password)
            login(request, usuario)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'usuarios/cadastro.html', context)

def logout_view(request):
    '''
    Possibilita o logout.
    '''

    logout(request)
    return redirect('home')

def login_view(request):
    '''
    Possibilita o login do usuário.
    '''

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, 'usuarios/login.html', context)


