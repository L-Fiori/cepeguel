from django.shortcuts import render, redirect

from artigo.models import TipoDeProduto, Produto

from carrinho.models import Order, OrderItem

from .forms import ProdutoForm

# Create your views here.

def produto_create_view(request):
    form = ProdutoForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProdutoForm()

    context = {
        'form': form
    }
    return render(request, "produto_create.html", context)


def produto_detail_view(request, ide):
    obje = TipoDeProduto.objects.get(id=ide)
    context = {
        'obj': obje
    }
    return render(request, "produto_detail.html", context)


def produto_update(request, ide):
    produto = TipoDeProduto.objects.get(id=ide)
    form = ProdutoForm(instance=produto)

    if (request.method == 'POST'):
        form = ProdutoForm(request.POST, instance = produto)
        if form.is_valid():
           form.save()
           return redirect ('/')

    context={'form': form}
    return render(request, "produto_create.html", context)

# ------- Carrinho -----------------------
def modalidades(request):
    object_list = TipoDeProduto.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.id, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, 'artigo/produto.html', context)