from django.db import models
from pathlib import Path


class Produto(models.Model):
    tipo     = models.ForeignKey('TipoDeProduto', on_delete=models.CASCADE, help_text="Tipo no qual o produto se enquadra")
    nome     = models.CharField(max_length=100, null=True, help_text="Nome do produto")
    foto     = models.ImageField(upload_to = 'fotosdeartigo', max_length=300, help_text="Foto do produto")
    disp     = models.BooleanField(help_text="Verdadeiro se o produto está disponível")
    alug     = models.BooleanField(help_text="Verdadeiro se o produto está alugado")
    rese     = models.BooleanField(help_text="Verdadeiro se o produto está reservado")
    pack     = models.IntegerField(default=1, help_text="Indica quantas unidades do produto são utilizados por aluguel")

    def __str__(self):
        return self.nome

class Modalidade(models.Model):
    nome     = models.CharField(max_length=100, unique=True, null=True, help_text="Nome da modalidade")

    def __str__(self):
        return self.nome

class TipoDeProduto(models.Model):
    nome     = models.CharField(max_length = 100, help_text="Nome do tipo de produto considerado")
    modalidade  = models.ForeignKey('Modalidade', on_delete=models.CASCADE, default="1", help_text="Modalidade na qual o tipo de produto se enquadra")

    class Meta:
        verbose_name_plural = "Tipos de produtos"

    def __str__(self):
        return self.nome

