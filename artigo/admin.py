from django.contrib import admin
from .models import Produto, TipoDeProduto, Modalidade

# Register your models here.

admin.site.register(Produto)
admin.site.register(TipoDeProduto)
admin.site.register(Modalidade)