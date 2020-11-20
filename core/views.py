from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from artigo.models import TipoDeProduto
from usuarios.models import Usuario

# Create your views here.
def home(request):
    context = {}
    
    return render(request, 'core/menu.html', context)

def modalidades(request):
    obj=TipoDeProduto.objects.all()
    context = {'obj': obj}

    return render(request, 'core/modalidades.html', context)

def produtosdemodalidade(request):
    obj=TipoDeProduto.objects.all()
    context = {'obj': obj}

    return render(request, 'core/produtosdemodalidade.html', context)

def cestadeprodutos(request):
    obj=TipoDeProduto.objects.all()
    context = {'obj': obj}

    return render(request, 'carrinho/cestadeprodutos.html', context)

def login(request):
    context = {}

    return render(request, 'core/login.html', context)

def produto(request):
    context = {}

    return render(request, 'core/produto.html', context)

