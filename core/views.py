from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from artigo.models import TipoDeProduto, Modalidade, Produto
from usuarios.models import Usuario
from carrinho.models import Order, OrderItem
from aluguel.models import Aluguel


# Create your views here.

def check_time():
    users = Usuario.objects.all()
    for user in users:
        my_user_profile = Usuario.objects.filter(email=user).first()
        user_rents = Aluguel.objects.filter(usuario=my_user_profile)
        for ordeer in user_rents:
            Aluguel.delete_after_one_or_five_hours(ordeer)
            if ordeer.rent_in_process == False:
                aluguel = get_object_or_404(Aluguel, id=ordeer.id)
                aluguel.delete()

def home(request):
    check_time()
    context = {}
    return render(request, 'core/menu.html', context)

def modalidades(request):
    check_time()
    modalidades = Modalidade.objects.all()
    context = {'modalidades': modalidades}

    return render(request, 'core/modalidades.html', context)

def produtosdemodalidade(request, id):
    check_time()
    produtosdemodalidade = TipoDeProduto.objects.filter(modalidade=id)
    context = {'produtosdemodalidade': produtosdemodalidade,
               'id_antigo': id} 

    return render(request, 'core/produtosdemodalidade.html', context)

def produtos(request, id_antigo, id):
    check_time()
    produtos = Produto.objects.filter(tipo=id)
    context = {'produtos': produtos,
               'id_antigo2': id_antigo,
               'id_antigo1': id}

    return render(request, 'core/produtos.html', context)

def get_user_pending_order(request):
    user_profile = get_object_or_404(Usuario, email=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order:
        return order[0]
    return 0

def produto(request, id_antigo2, id_antigo1, item_id):
    check_time()
    my_user_profile = Usuario.objects.filter(email=request.user).first()
    obj = Produto.objects.get(id=item_id)
    filtered_orders = Order.objects.filter(owner=request.user.id, is_ordered=False)
    current_order_products = []
    alugou = False
    professor = my_user_profile.is_professor
    user_rents = Aluguel.objects.filter(usuario=my_user_profile)
    li_user_rents = list(user_rents)
    idprodutos = list(user_rents.values_list('prod'))
    listaidprodutos = []
    existing_order = get_user_pending_order(request)
    lista_de_produtos = 0
    if (existing_order != 0): lista_de_produtos = existing_order.get_cart_total()
    for i in idprodutos:
        for j in i:
            num = ""         ## se você está lendo isso, sinceramente me desculpe
            if type(j) == int:    
                num += str(j) 
        listaidprodutos.append(int(num))
    if (len(li_user_rents)+lista_de_produtos) >= 3 and not professor and len(li_user_rents) != 0:
        alugou = True
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]
        tamanho = len(current_order_products)
    context = {
    'obj': obj,
    'current_order_products': current_order_products,
    'tamanho':tamanho,
    'professor':professor,
    'alugou': alugou,
    'listaidprodutos':listaidprodutos,
    'lista_de_produtos':lista_de_produtos,
    }

    return render(request, 'core/produto.html', context)

def cestadeprodutos(request):
    check_time()
    obj=TipoDeProduto.objects.all()
    context = {'obj': obj}

    return render(request, 'carrinho/cestadeprodutos.html', context)

def login(request):
    check_time()
    context = {}

    return render(request, 'core/login.html', context)

def reservados(request):
    check_time()
    list_alug = []
    alugueis = Aluguel.objects.all()
    for aluguel in alugueis:
        if aluguel.prod.rese == True:
            list_alug.append(aluguel)
    context = {
        'reserva':list_alug,
    }

    return render(request,'core/reservados.html', context)