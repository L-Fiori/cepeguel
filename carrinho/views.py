import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from core.views import produto

from usuarios.models import Usuario, ManagerDoUsuario
from artigo.models import TipoDeProduto, Produto
from aluguel.models import Aluguel

from carrinho.extras import generate_order_id
from carrinho.models import OrderItem, Order

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

def get_user_pending_order(request):
    user_profile = get_object_or_404(Usuario, email=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order:
        return order[0]
    return 0

def add_to_cart(request, **kwargs):
    check_time()
    my_user_profile = Usuario.objects.filter(email=request.user).first()
    existing_order = get_user_pending_order(request)
    lista_de_produtos = 0
    user_rents = list(Aluguel.objects.filter(usuario=my_user_profile))
    if (existing_order != 0): lista_de_produtos = existing_order.get_cart_total()
    if ( lista_de_produtos < 3 or my_user_profile.is_professor or (user_rents+lista_de_produtos) >= 3):
    
        # get the user profile
        user_profile = get_object_or_404(Usuario, email=request.user)
        # filter products by id
        product = Produto.objects.filter(id=kwargs.get('item_id', "")).first()
        # create orderItem of the selected product
        order_item, status = OrderItem.objects.get_or_create(product=product)
        # create order associated with the user
        user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
        user_order.items.add(order_item)
        if status:
            # generate a reference code
            user_order.ref_code = generate_order_id()
            user_order.save()

        # show confirmation message and redirect back to the same page
        messages.info(request, "item added to cart")
        return redirect(reverse('carrinho:order_details'))
        
    else:
        return redirect(reverse('carrinho:order_details'))

def delete_from_cart(request, item_id):
    check_time()
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('carrinho:order_details'))


def order_details(request, **kwargs):
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

def checkout(request, **kwargs):
    client_token = generate_client_token()
    existing_order = get_user_pending_order(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=100*existing_order.get_cart_total(),
                    currency='usd',
                    description='Example charge',
                    source=token,
                )

                return redirect(reverse('carrinho:order_details',
                        kwargs={
                            'token': token
                        })
                    )
            except stripe.CardError as e:
                message.info(request, "Your card has been declined.")
        else:
            result = transact({
                'amount': existing_order.get_cart_total(),
                'payment_method_nonce': request.POST['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                return redirect(reverse('carrinho:order_details',
                        kwargs={
                            'token': result.transaction.id
                        })
                    )
            else:
                for x in result.errors.deep_errors:
                    messages.info(request, x)
                return redirect(reverse('carrinho:order_details'))
            
    context = {
        'order': existing_order,
        'client_token': client_token,
        'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'carrinho/cestadeprodutos.html', context)


def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(Usuario, user=request.user)
    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.meus_alugueis.add(*order_products)
    user_profile.save()

    
    # create a transaction
    transaction = Transaction(profile=request.user.profile,
                            token=token,
                            order_id=order_to_purchase.id,
                            amount=order_to_purchase.get_cart_total(),
                            success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()


    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('carrinho:order_details'))


def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'carrinho/cestadeprotudos.html', {})


def aluguel_carrinho(request):
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
    return redirect(reverse('core:modalidades'))