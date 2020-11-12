from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    
    return render(request, 'core/menu.html', context)

def modalidades(request):
    context = {}

    return render(request, 'core/modalidades.html', context)


def cestadeprodutos(request):
    context = {}

    return render(request, 'core/cestadeprodutos.html', context)

def login(request):
    context = {}

    return render(request, 'core/login.html', context)

def cadastro(request):
    context = {}

    return render(request, 'core/cadastro.html', context)