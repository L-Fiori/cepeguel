from django.urls import path
from django.conf.urls import url

from .views import check_time_artigo

app_name = 'artigo'

urlpatterns = [
    path('', check_time_artigo, name='check_time_artigo'),
]