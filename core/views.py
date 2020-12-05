from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from artigo.models import TipoDeProduto, Modalidade, Produto
from usuarios.models import Usuario
from carrinho.models import Order, OrderItem

# Create your views here.
def home(request):
    context = {}
    
    return render(request, 'core/menu.html', context)

def modalidades(request):
    modalidades = Modalidade.objects.all()
    context = {'modalidades': modalidades}

    return render(request, 'core/modalidades.html', context)

def produtosdemodalidade(request, id):
    produtosdemodalidade = TipoDeProduto.objects.filter(modalidade=id)
    context = {'produtosdemodalidade': produtosdemodalidade,
               'id_antigo': id} 

    return render(request, 'core/produtosdemodalidade.html', context)

def produtos(request, id_antigo, id):
    produtos = Produto.objects.filter(tipo=id)
    context = {'produtos': produtos,
               'id_antigo2': id_antigo,
               'id_antigo1': id}

    return render(request, 'core/produtos.html', context)

def produto(request, id_antigo2, id_antigo1, item_id):
    obj = Produto.objects.get(id=item_id)
    filtered_orders = Order.objects.filter(owner=request.user.id, is_ordered=False)
    current_order_products = []

    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'obj': obj,
        'current_order_products': current_order_products
    }

    return render(request, 'core/produto.html', context)

def cestadeprodutos(request):
    obj=TipoDeProduto.objects.all()
    context = {'obj': obj}

    return render(request, 'carrinho/cestadeprodutos.html', context)

def login(request):
    context = {}

    return render(request, 'core/login.html', context)