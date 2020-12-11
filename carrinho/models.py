from __future__ import unicode_literals
from django.db import models
from pathlib import Path

from usuarios.models import Usuario
from artigo.models import TipoDeProduto, Produto


class OrderItem(models.Model):
    product = models.OneToOneField(Produto, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.nome
    
class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, help_text="Usuário associado à cesta de produtos")
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem, help_text="Produtos que estão no carrinho do usuário")
 
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        '''
        Retorna uma QuerySet com os objetos contidos no carrinho.
        '''

        return self.items.all()

    def get_cart_total(self):
        '''
        Retorna o número de objetos contidos no carrinho.
        '''

        return self.items.all().count()

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)
