# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from .models import NeuralNet, Prediction, DataSet, Quote
from nets.netManagement import loadNet
from datetime import timedelta
from django.utils.timezone import now
from django.views.generic import View
import json


class SetOffsetView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        offset = request.POST.get('offset', None)
        if not offset:
            return HttpResponse("No 'offset' parameter provided", status=400)

        try:
            offset = int(offset)
        except ValueError:
            return HttpResponse("Invalid 'offset' value provided", status=400)

        request.session['detected_tz'] = int(offset)

        return HttpResponse("OK")


# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'neironet_info': 'a',
    })
    return HttpResponse(template.render(context))


def neironets(request):
    neironet_list = NeuralNet.objects.order_by('-creation_date')
    template = loader.get_template('neironets.html')
    context = RequestContext(request, {
        'neironet_list': neironet_list,
    })
    return HttpResponse(template.render(context))


def neironet_detail(request, neironet_id):
    neironet_info = NeuralNet.objects.get(pk=neironet_id)
    inputs_range = range(neironet_info.number_of_inputs)
    number_of_days = 7
    cbr_quotes = []
    quote_dates = []
    predicted_quotes = []
    today = now().date()
    for delta in range(number_of_days, -2, -1):
        print delta
        prediction_qs = Prediction.objects.filter(neiro_net=neironet_info, predicted_on_date=today-timedelta(days=delta),
                                               prediction_is_automate='Y').order_by('predicted_on_date')
        cbr_quote_qs = Quote.objects.filter(quote_date=today - timedelta(days=delta), quote_type='usd').order_by('quote_date')
        quote_dates.append(str(today-timedelta(days=delta)))
        if prediction_qs:
            predicted_quotes.append(str(prediction_qs[0].output_data))
        else:
            predicted_quotes.append(None)
        if cbr_quote_qs:
            cbr_quotes.append(str(cbr_quote_qs[0].quote_value))
        else:
            cbr_quotes.append(None)
    template = loader.get_template('neironet_detail.html')
    context = RequestContext(request, {
        'neironet_info': neironet_info, 'inputs_range': inputs_range, 'cbr_quotes': json.dumps(cbr_quotes).replace('"', ''),
        'quote_dates': quote_dates, 'predicted_quotes': json.dumps(predicted_quotes).replace('"', '')
    })
    return HttpResponse(template.render(context))


def predict(request, neironet_id):
    net = get_object_or_404(NeuralNet, pk=neironet_id)
    try:
        loaded_net = loadNet(net.neironet_file)
        data_list = []
        data_string = ""
        for i in range(0, net.number_of_inputs):
            value = request.POST['quote_' + str(i)].replace(',', '.').strip()
            data_list.append(float(value))
            data_string += value + ', '
        prediction_result = loaded_net.activate(data_list)[0]
        print prediction_result
    except (IOError, NeuralNet.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('neironet_detail.html', {
            'net': net,
            'error_message': "Wrong net file.",
        }, context_instance=RequestContext(request))
    else:
        pred = Prediction(neiro_net=net, input_data=data_string[:-2], output_data=prediction_result,
                          predicted_on_date=now().date()+timedelta(days=1))
        pred.save()
        context = RequestContext(request, {
        'prediction': pred,
    })
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('prediction_research.views.prediction_detail', args=(pred.id,)))


def predictions(request):
    predictions_list = Prediction.objects.order_by('-prediction_date')
    template = loader.get_template('predictions.html')
    context = RequestContext(request, {
        'predictions_list': predictions_list,
    })
    return HttpResponse(template.render(context))


def prediction_detail(request, prediction_id):
    prediction = Prediction.objects.get(pk=prediction_id)
    template = loader.get_template('prediction_detail.html')
    context = RequestContext(request, {
        'prediction': prediction,
    })
    return HttpResponse(template.render(context))


def datasets(request):
    dataset_list = DataSet.objects.order_by('-data_set_on_date')[::-1]
    template = loader.get_template('datasets.html')
    context = RequestContext(request, {
        'dataset_list': dataset_list, 'debug_list': debug_list
    })
    return HttpResponse(template.render(context))