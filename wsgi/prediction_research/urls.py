# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^neironets/$', views.neironets, name='neironets'),
    url(r'^neironets/(?P<neironet_id>\d+)/$', views.neironet_detail, name='neironet_detail'),
    url(r'^neironets/(?P<neironet_id>\d+)/predict/$', views.predict, name='predict'),
    url(r'^predictions/(?P<prediction_id>\d+)/$', views.prediction_detail, name='prediction_detail'),
    url(r'^datasets/$', views.datasets, name='datasets'),
    url(r'^predictions/$', views.predictions, name='predictions'),
    url(r'^set/$', views.SetOffsetView.as_view(), name="tz_detect__set"),
]