import datetime

from django.db import models
from django.utils import timezone

from pathlib import Path
from artigo.models import Produto, TipoDeProduto

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your models here.

class Aluguel(models.Model):
    atleta          = "Atleta"
    treinador       = "Treinador"
    usuarios        = [(atleta, "Atleta"),(treinador,"Treinador")]
    tipo_usr        = models.CharField(max_length=9,choices=usuarios,default=atleta)
    tipo_prod       = models.ForeignKey(TipoDeProduto, on_delete=models.CASCADE)
    qtd             = models.IntegerField()
    hora            = models.IntegerField()
    created_at      = models.DateField(default=timezone.now)
    user_takeout    = models.BooleanField(default=False)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Aluguéis"


'''

Provavelmente não vamos precisar da implementação do ItemDeAluguel,
mas ta aqui pra não se perder caso formos precisar

produto   = models.ManyToManyField(Produto, through='ItemDeAluguel')

class ItemDeAluguel(models.Model):
    aluguel = models.ForeignKey(Aluguel, default="deafult", on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, default="default", on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Itens De Aluguel"

'''
