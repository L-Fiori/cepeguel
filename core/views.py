from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    
    return render(request, 'core/base.html', context)

def modalidades(request):
    context = {}

    return render(request, 'core/modalidades.html', context)

def menu(request):
    context = {}

    return render(request, 'core/menu.html', context)

def cestadeprodutos(request):
    context = {}

    return render(request, 'core/cestadeprodutos.html', context)