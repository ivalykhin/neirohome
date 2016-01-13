# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^neironets/$', views.neironets, name='neironets'),
    url(r'^neironets/(?P<neironet_id>[0-9]+)/$', views.neironet_detail, name='neironet_detail'),
    url(r'^datasets/$', views.datasets, name='datasets'),
    url(r'^predictions/$', views.predictions, name='predictions'),
]