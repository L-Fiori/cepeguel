from django.db import models
from pathlib import Path
from artigo.models import TipoDeProduto

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your models here.

class Aluguel(models.Model):
    atleta = "Atleta"
    treinador = "Treinador"
    usuarios = [(atleta, "Atleta"),(treinador,"Treinador")]
    tipo_usr  = models.CharField(max_length=9,choices=usuarios,default=atleta)
    tipo_prod = models.ForeignKey(TipoDeProduto, on_delete=models.CASCADE)
    qtd       = models.IntegerField()
    hora      = models.IntegerField()
    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Aluguéis"

class ItemDeAluguel(models.Model):
    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Itens De Aluguel"


