"""cepeguel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from core.views import (
    cestadeprodutos,
    home,
    modalidades,
    login,
    produtosdemodalidade,
    produto,
)

from usuarios.views import (
    registration_view,
    logout_view,
    login_view,
)

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('aluguel/', include('aluguel.urls')),
    path('cestadeprodutos/', include('carrinho.urls', namespace='carrinho')),
    path('cadastro/', registration_view, name='cadastro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),
    path('modalidades/', include('core.urls', namespace='core')),
    ]

