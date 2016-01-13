# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import NeiroNet, Prediction, DataSets


# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'neironet_info': 'a',
    })
    return HttpResponse(template.render(context))


def neironets(request):
    neironet_list = NeiroNet.objects.order_by('-creation_date')
    template = loader.get_template('neironets.html')
    context = RequestContext(request, {
        'neironet_list': neironet_list,
    })
    return HttpResponse(template.render(context))


def neironet_detail(request, neironet_id):
    neironet_info = NeiroNet.objects.get(pk=neironet_id)
    template = loader.get_template('neironet_detail.html')
    context = RequestContext(request, {
        'neironet_info': neironet_info,
    })
    return HttpResponse(template.render(context))


def predictions(request):
    predictions_list = Prediction.objects.order_by('-prediction_date')
    template = loader.get_template('predictions.html')
    context = RequestContext(request, {
        'predictions_list': predictions_list,
    })
    return HttpResponse(template.render(context))


def prediction_detail(request, prediction_id):
    prediction_info = Prediction.objects.get(pk=prediction_id)
    template = loader.get_template('prediction_detail.html')
    context = RequestContext(request, {
        'prediction_info': prediction_info,
    })
    return HttpResponse(template.render(context))


def datasets(request):
    dataset_list = DataSets.objects.order_by('-data_set_on_date')[::-1]
    template = loader.get_template('datasets.html')
    context = RequestContext(request, {
        'dataset_list': dataset_list,
    })
    return HttpResponse(template.render(context))