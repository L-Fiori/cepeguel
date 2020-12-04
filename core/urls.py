from django.urls import path
from django.conf.urls import url

from .views import produto, modalidades, produtosdemodalidade

app_name = 'core'

urlpatterns = [
    path('', modalidades, name='modalidades'),
    url(r'^(?P<modalidade_nome>[-\w]+)/$', produtosdemodalidade, name='produtosdemodalidade'),
    #url(r'^(?P<item_id>[-\w]+)/$', produto, name='produto'),
    #url(r'^', produto, name='produto')
]