import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from core.views import produto, check_time, get_user_pending_order

from usuarios.models import Usuario, ManagerDoUsuario
from artigo.models import TipoDeProduto, Produto
from aluguel.models import Aluguel

from carrinho.models import OrderItem, Order


def add_to_cart(request, **kwargs):
    '''
    Função que checa se o usuário é apto a adicionar itens ao carrinho e, em caso afirmativo,
    adiciona um item ao carrinho dele.
    '''

    check_time()
    my_user_profile = Usuario.objects.filter(email=request.user).first()
    existing_order = get_user_pending_order(request)
    user_rents = list(Aluguel.objects.filter(usuario=my_user_profile))
    lista_de_produtos = existing_order.get_cart_total() if existing_order != 0 else 0
    if (lista_de_produtos < 3 or my_user_profile.is_professor or (user_rents+lista_de_produtos) >= 3) and \
        my_user_profile.is_able_to_rent:
        # pega o perfil de usuário
        user_profile = get_object_or_404(Usuario, email=request.user)
        # filtra produtos pelo id
        product = Produto.objects.filter(id=kwargs.get('item_id', "")).first()
        # cria um OrderItem do produto selecionado
        order_item, status = OrderItem.objects.get_or_create(product=product)
        # cria Order associado ao usuário
        user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
        user_order.items.add(order_item)
        if status:
            user_order.save()

        return redirect(reverse('carrinho:order_details'))
    else:
        return redirect(reverse('carrinho:order_details'))

def delete_from_cart(request, item_id):
    '''
    Deleta um item do carrinho.
    '''

    check_time()
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('carrinho:order_details'))

def order_details(request, **kwargs):
    '''
    View da cesta. Entrega para o layout todas as informações necessárias acerca do carrinho do usuário.
    '''

    check_time()
    my_user_profile = Usuario.objects.filter(email=request.user).first()
    existing_order = get_user_pending_order(request)
    soma_pedidos = 0
    if (existing_order != 0): soma_pedidos = existing_order.get_cart_total()
    if (soma_pedidos < 3 or my_user_profile.is_professor): aviso = False
    else: aviso = True

    context = {
        'aviso': aviso,
        'order': existing_order
    }

    return render(request, 'carrinho/cestadeprodutos.html', context)

def aluguel_carrinho(request):
    '''
    Essa view estabelece a união entre o layout da cesta de produtos e a instanciação de objetos
    do tipo Aluguel.
    '''

    check_time()
    context = {}
    produtos = []

    # Primeiro tem que ver qual user tá querendo alugar
    my_user_profile = Usuario.objects.filter(email=request.user).first()

    # Depois tem que ver qual é o carrinho do user (quais itens, qual a Order)
    existing_order = get_user_pending_order(request)
    items = existing_order.get_cart_items()

    for item in items:
        produtos.append(Produto.objects.get(nome=item))

    # Daí instancia um objeto aluguel para CADA ITEM DO ORDER
    for produto in produtos:
        Aluguel.objects.create(usuario=my_user_profile, prod=produto)
        produto.disp = False
        produto.rese = True
        produto.save(update_fields=["disp", "rese"]) 
        # Depois deleta todos os itens do carrinho
        item_to_delete = OrderItem.objects.filter(product=produto)
        if item_to_delete.exists():
            item_to_delete[0].delete()
            
    # Mostrar nova cesta de produtos
    return redirect(reverse('core:reservados'))