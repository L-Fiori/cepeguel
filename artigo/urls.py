from django.urls import path
from django.conf.urls import url

from .views import modalidades

app_name = 'artigo'

urlpatterns = [
    url(r'^(?P<item_id>[-\w]+)/$', modalidades, name='modalidades')
    #url(r'^', modalidades, name='modalidades')

]