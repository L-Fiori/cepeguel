from django.urls import path
from django.conf.urls import url

app_name = 'carrinho'

from .views import (
    add_to_cart,
    delete_from_cart,
    order_details,
    aluguel_carrinho
)

urlpatterns = [
    path('teste/', aluguel_carrinho, name='aluguel_carrinho'),
    url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', add_to_cart, name="add_to_cart"),
    url(r'^item/delete/(?P<item_id>[-\w]+)/$', delete_from_cart, name='delete_item'),
    url(r'^', order_details, name='order_details')
]