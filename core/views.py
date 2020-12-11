from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from artigo.models import TipoDeProduto, Modalidade, Produto
from usuarios.models import Usuario
from carrinho.models import Order, OrderItem
from aluguel.models import Aluguel


def get_user_pending_order(request):
    user_profile = get_object_or_404(Usuario, email=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order:
        return order[0]
    return 0

def check_time():
    '''
    Verifica o tempo dos aluguéis criados pra ver se já expirou.
    '''
    
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
    '''
    View da página inicial, nada demais.
    '''

    check_time()
    context = {}
    return render(request, 'core/menu.html', context)

def modalidades(request):
    '''
    View que entrega à página os nomes das modalidades nas quais 
    o sistema possui produtos.
    '''

    check_time()
    modalidades = Modalidade.objects.all()
    context = {'modalidades': modalidades}

    return render(request, 'core/modalidades.html', context)

def produtos_de_modalidade(request, id):
    '''
    View que entrega à página os tipos de produto associados à modalidade
    selecionada pelo usuário. Parâmetro id necessário para gerar a 
    url dinâmica.
    '''

    check_time()
    produtos_de_modalidade = TipoDeProduto.objects.filter(modalidade=id)
    context = {'produtos_de_modalidade': produtos_de_modalidade,
               'id_antigo': id} 

    return render(request, 'core/produtos_de_modalidade.html', context)

def produtos(request, id_antigo, id):
    '''
    View que entrega à pagina os produtos associados ao tipo de produto 
    selecionado pelo usuário. Parâmetros id e id_antigo necessários para
    gerar a url dinâmica.
    '''

    check_time()
    produtos = Produto.objects.filter(tipo=id)
    context = {'produtos': produtos,
               'id_antigo2': id_antigo,
               'id_antigo1': id}

    return render(request, 'core/produtos.html', context)

def produto(request, id_antigo2, id_antigo1, item_id):
    '''
    View que entrega à página tanto as informações do produto quanto as informações
    necessárias para decidir se o usuário pode ou não fazer reservas, e avisá-lo
    conforme o requisito que ele não cumpre. Parâmetros id e id_antigo necessários 
    para gerar a url dinâmica.
    '''

    check_time()
    alugou = False
    my_user_profile = Usuario.objects.filter(email=request.user).first()
    user_rents = Aluguel.objects.filter(usuario=my_user_profile)
    id_produtos = list(user_rents.values_list('prod'))

    # Necessário tratar a QuerySet para entregar a lista com os ids dos produtos alugados pelo usuário
    # para a página.
    lista_id_produtos = []
    for i in id_produtos:
        for j in i:
            num = ""
            if type(j) == int:
                num += str(j) 
        lista_id_produtos.append(int(num))

    existing_order = get_user_pending_order(request)
    lista_de_produtos = existing_order.get_cart_total() if existing_order != 0 else 0
    li_user_rents = list(user_rents)
    if (len(li_user_rents)+lista_de_produtos) >= 3 and not my_user_profile.is_professor and len(li_user_rents) != 0:
        alugou = True

    # Entrega a quantidade de produtos e a lista de produtos que
    # constam no carrinho do usuário no momento.
    current_order_products = []
    filtered_orders = Order.objects.filter(owner=request.user.id, is_ordered=False)
    tamanho = 0
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]
        tamanho = len(current_order_products)

    # Por fim, obviamente, entrega o próprio objeto do tipo Produto em questão.
    obj = Produto.objects.get(id=item_id)

    context = {
    'obj': obj,
    'current_order_products': current_order_products,
    'tamanho':tamanho,
    'professor':my_user_profile.is_professor,
    'alugou': alugou,
    'lista_id_produtos':lista_id_produtos,
    'lista_de_produtos':lista_de_produtos,
    }

    return render(request, 'core/produto.html', context)

def cestadeprodutos(request):
    '''
    View da cesta de produtos.
    '''

    check_time()
    obj=TipoDeProduto.objects.all()
    context = {'obj': obj}

    return render(request, 'carrinho/cestadeprodutos.html', context)

def reservados(request):
    '''
    View da página "Reservados". Entrega ao layout a lista de produtos reservados
    pelo usuário e também a reserva mais antiga, para que o tempo da sua primeira
    reserva seja contabilizado no reloginho da página.
    '''

    check_time()
    list_alug = []
    my_user_profile = Usuario.objects.filter(email=request.user).first()
    alugueis = Aluguel.objects.filter(usuario=my_user_profile)
    for aluguel in alugueis:
        if aluguel.prod.rese == True:
            list_alug.append(aluguel)
    reserva1=[]
    if list_alug:
        reserva1 = list_alug[0]
    context = {
        'reserva':list_alug,
        'reserva1':reserva1,
    }

    return render(request,'core/reservados.html', context)