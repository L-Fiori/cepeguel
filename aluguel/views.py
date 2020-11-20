from django.shortcuts import render, redirect

from artigo.models import *
from .models import *
from .forms import AluguelForm
from artigo.forms import ProdutoForm
from artigo.views import produto_create_view

def aluguel_create_view(request, ide):
    form = AluguelForm()
    obj = TipoDeProduto.objects.get(id=ide)
    form2 = ProdutoForm(instance=obj)

    if (request.method == 'POST'):
        form = AluguelForm(request.POST)
        form2 = ProdutoForm(request.POST, instance=obj)
        if form.is_valid():
           form.save()
           form = AluguelForm()
        if form2.is_valid():
            obj.qtd_disp = 0
            form2.save()
    context = {
        'form': form,
        'obj': obj,
    }

    return render(request, "aluguel_create.html", context)


