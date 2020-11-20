from django import forms

from .models import Produto, TipoDeProduto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = TipoDeProduto
        fields = [
            'nome',
            'esporte',
            'qtd_disp'
        ]