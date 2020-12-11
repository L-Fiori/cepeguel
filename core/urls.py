from django.urls import path
from django.conf.urls import url

from .views import produto, modalidades, produtos_de_modalidade, produtos

app_name = 'core'

urlpatterns = [
    path('', modalidades, name='modalidades'),
    path('<int:id>/', produtos_de_modalidade, name='produtos_de_modalidade'),
    path('<int:id_antigo>/<int:id>/', produtos, name='produtos'),
    path('<int:id_antigo2>/<int:id_antigo1>/<int:item_id>', produto, name='produto')
]