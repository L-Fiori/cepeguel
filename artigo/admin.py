from django.contrib import admin
from .models import Produto, TipoDeProduto, Modalidade
from django import forms
from django.urls import path
from django.http import HttpResponse


class ProdutoAdminForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = "__all__"


def make_disponivel(modeladmin, request, queryset):
    '''
    Implementa a possibilidade de o administrador mudar o atributo "disp" para
    True, "rese" e "alug" para False de vários objetos da classe Produto 
    simultaneamente.
    '''

    queryset.update(disp=True)
    queryset.update(rese=False)
    queryset.update(alug=False)
make_disponivel.short_description = "Marcar todos os produtos como disponíveis"

def make_reservado(modeladmin, request, queryset):
    '''
    Implementa a possibilidade de o administrador mudar o atributo "rese" para
    True, "disp" e "alug" para False de vários objetos da classe Produto 
    simultaneamente.
    '''

    queryset.update(rese=True)
    queryset.update(disp=False)
    queryset.update(alug=False)
make_reservado.short_description = "Marcar todos os produtos como reservados"

def make_alug(modeladmin, request, queryset):
    '''
    Implementa a possibilidade de o administrador mudar o atributo "alug" para
    True, "disp" e "rese" para False de vários objetos da classe Produto 
    simultaneamente.
    '''

    queryset.update(rese=False)
    queryset.update(disp=False)
    queryset.update(alug=True)
make_alug.short_description = "Marcar todos os produtos como alugados"


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    '''
    Customização da página do admin.
    '''
    list_display = ("tipo", "nome", "disp", "rese", "alug", "pack")
    form = ProdutoAdminForm
    actions = [make_disponivel, make_reservado, make_alug]
    list_filter = ("tipo",)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form


admin.site.register(TipoDeProduto)
admin.site.register(Modalidade)