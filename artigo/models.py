# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

    def __str__(self):
        return self.tipo

class Modalidade(models.Model):
    nome     = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return self.nome

class TipoDeProduto(models.Model):
    nome     = models.CharField(max_length = 100)
    modalidade  = models.ForeignKey('Modalidade', on_delete=models.CASCADE, default="1")

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Tipos de produtos"

    def __str__(self):
        return self.nome





