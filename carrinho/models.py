from __future__ import unicode_literals
from django.db import models
from pathlib import Path

from usuarios.models import Usuario
from artigo.models import TipoDeProduto

# Create your models here.

class OrderItem(models.Model):
    product = models.OneToOneField(TipoDeProduto, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.nome
    
class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    # Form de Aluguel
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.qtd_disp for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)