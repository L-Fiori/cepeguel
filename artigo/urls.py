from django.urls import path
from django.conf.urls import url

from .views import check_time

app_name = 'artigo'

urlpatterns = [
    path('', check_time, name='check_time'),
]

#url(r'^$', check_time, name='check_time'), 