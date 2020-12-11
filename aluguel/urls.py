from django.urls import path
from django.conf.urls import url

from .views import check_time_admin

app_name = 'aluguel'

urlpatterns = [
    path('', check_time_admin, name='check_time_admin'),
]