from .models import Aluguel
from usuarios.models import Usuario
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def check_time(request):
    users = Usuario.objects.all()
    for user in users:
        my_user_profile = Usuario.objects.filter(email=user).first()
        user_rents = Aluguel.objects.filter(usuario=my_user_profile)
        for order in user_rents:
            Aluguel.delete_after_one_or_five_hours(order)
            if order.rent_in_process == False:
                aluguel = get_object_or_404(Aluguel, id=order.id)
                aluguel.delete()

    return redirect('../admin/aluguel/aluguel')
    