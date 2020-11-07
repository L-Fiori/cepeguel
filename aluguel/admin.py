from django.contrib import admin
from .models import Aluguel
from .models import ItemDeAluguel

# Register your models here.

admin.site.register(Aluguel)
admin.site.register(ItemDeAluguel)