from aluguel.models import Aluguel
from usuarios.models import Usuario
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from core.views import check_time

def check_time_artigo(request):
    '''
    Verifica o tempo dos aluguéis criados pra ver se já expirou.
    '''
    
    check_time()

    return redirect('../admin/artigo/produto')