from django.db import models
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your models here.

class Produto(models.Model):
    tipo     = models.ForeignKey('TipoDeProduto', on_delete=models.CASCADE)
    foto     = models.FileField(upload_to = '{}/fotos/fotosdeartigo'.format(BASE_DIR),max_length=100)
    disp     = models.BooleanField()
    alug     = models.BooleanField()
    rese     = models.BooleanField()

class TipoDeProduto(models.Model):
    nome     = models.CharField(max_length = 100)
    esporte  = models.CharField(max_length = 100)
    qtd_disp = models.IntegerField()
    qtd_alug = models.IntegerField()
    qtd_rese = models.IntegerField()
    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Tipos de produtos"
    def __str__(self):
        return self.nome





