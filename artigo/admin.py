from django.contrib import admin
from .models import Produto
from .models import TipoDeProduto

# Register your models here.

admin.site.register(Produto)
admin.site.register(TipoDeProduto)