from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from django.conf.urls import url
from django.urls import path
from django.http import HttpResponse
from .models import Aluguel
from usuarios.models import Usuario
from django import forms
from artigo.models import Produto

# Register your models here.

admin.site.site_header = 'Administração do Cepe - Cepeguel 2020 - Universidade de São Paulo'

class AluguelAdminForm(forms.ModelForm):
    class Meta:
        model = Aluguel
        fields = "__all__"

    def clean(self):
        prodd  = self.cleaned_data.get('prod')
        order = Aluguel.objects.get(prod=prodd )
        if self.cleaned_data.get('rent_in_process')==False:
            Aluguel.delete_after_item_returned(order)            
            return

        elif self.cleaned_data.get('not_rented')==False:
            Aluguel.item_rented(order)
            return



def make_alugado(modeladmin, request, queryset):
    my_user_profile = Usuario.objects.filter(email=request.user).first()
    user_rents = Aluguel.objects.filter(usuario=my_user_profile)
    for order in user_rents:
        Aluguel.item_rented(order)
    queryset.update(not_rented=False)
make_alugado.short_description = "Marcar todos os aluguéis como alugados"


def make_not_alugado(modeladmin, request, queryset):
    queryset.update(not_rented=True)
make_not_alugado.short_description = "Marcar todos os aluguéis como não alugados"


def make_returned(modeladmin, request, queryset):
    my_user_profile = Usuario.objects.filter(email=request.user).first()
    user_rents = Aluguel.objects.filter(usuario=my_user_profile)
    for order in user_rents:
        Aluguel.delete_after_item_returned(order)   
    queryset.update(rent_in_process=False)
make_returned.short_description = "Marcar todos os aluguéis como encerrados"


@admin.register(Aluguel)
class AluguelAdmin(admin.ModelAdmin):
    list_display = ("usuario", "prod", "created_at", "rent_in_process", "not_rented", "rented_at")
    form = AluguelAdminForm
    actions = [make_alugado, make_not_alugado, make_returned]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["usuario"].label = "Email do meliante"
        return form

