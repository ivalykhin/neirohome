# -*- coding: utf-8 -*-
from celery.task import periodic_task
from celery.schedules import crontab
from datetime import timedelta
from .models import NeuralNet, DataSet, Training, TrainingResult, Quote, Prediction
from nets.netManagement import createAndTrainNetworkFromList, loadNet
from nets.getQuotesData import getCurrentOilQuotes, getUSDQuotesOnDate
from django.conf import settings
from django.utils.timezone import now


@periodic_task(run_every=crontab(minute='*/2'))
def createAndTrainNet():
    try:
        net_info = NeuralNet.objects.filter(training_epochs=0).order_by('-creation_date')[0]
    except IndexError:
        print "All networks are trained"
        net_info = []
    if net_info:
        print "Start trainig"
        training = Training(training_data_file='FromDB')
        training.neural_net = net_info
        training.save()
        net_info.training_epochs = 1
        net_info.save()
        dataset_list = DataSet.objects.order_by('-data_set_on_date')
        train_list = []
        for i in range(0, len(dataset_list)):
            temp_list = dataset_list[i].input_data.split(',')
            temp_list.append(str(dataset_list[i].output_data))
            train_list.append(temp_list)
        try:
            train_results = createAndTrainNetworkFromList(train_list, net_info.number_of_inputs,
                                                          settings.NEIRONET_STORAGE + net_info.name+'.xml',
                                                          max_epochs=1000)
            net_info.neironet_file = train_results[1]
            net_info.training_epochs += len(train_results[0][0])-3
            training.training_end_time = now()
            training_result = TrainingResult(training_epochs=len(train_results[0][1])-3, errors=train_results[0][0][-1])
            training_result.training = training
            net_info.save()
            training.save()
            training_result.save()
        except Exception as detail:
            print "Error: ", detail
            net_info.training_epochs = 0
            net_info.save()
            training.delete()


@periodic_task(run_every=crontab(minute=8, hour=10))
def quotesToDataSet(count_usd_quotes=4, count_oil_quotes=2, number_of_days_for_check=5):
    today = now().today()
    for delta in range(0, number_of_days_for_check):
        check_date = today - timedelta(days=delta)
        try:
            data_set = DataSet.objects.filter(data_set_on_date=check_date)[0]
            print "Dataset for date " + str(check_date) + " already exist: " + data_set.input_data
        except IndexError:

            """print "Dataset for date " + str(check_date) + " is absent. Generating..."
            quotes_list = Quote.objects.filter(quote_date__gt=check_date - timedelta(days=count_usd_quotes),
                                               quote_date__lte=check_date, quote_type='usd') | \
                          Quote.objects.filter(quote_date__gt=check_date - timedelta(days=count_oil_quotes),
                                               quote_date__lte=check_date, quote_type='brent')
            output_quote_list = Quote.objects.filter(quote_date=check_date + timedelta(days=1),
                                                     quote_type='usd').order_by('quote_date')"""
            """if len(quotes_list) == count_usd_quotes + count_oil_quotes and len(output_quote_list) > 0:
                output_quote = output_quote_list[0].quote_value
                input_data = ""
                for quote in quotes_list.order_by('-quote_type', 'quote_date'):
                    input_data += str(quote.quote_value) + ', '
                data_set = DataSet(data_set_on_date=check_date, input_data=input_data[:-2], output_data=output_quote)
                data_set.save()
            else:
                print "Number of quotes doesn't satisfy requirements"""

            print "Dataset on date " + str(check_date) + " is created"


@periodic_task(run_every=crontab(minute=5, hour=10))
def getTodayQuotes():
    today = now().date()
    try:
        brent_q = Quote.objects.get(quote_date=today, quote_type='brent')
        print "Brent quotes already exist today"
    except Quote.DoesNotExist:
        brent_quote_value = getCurrentOilQuotes()
        brent_q = Quote(quote_date=today, quote_value=brent_quote_value, quote_type='brent')
        brent_q.save()
    try:
        usd_q = Quote.objects.get(quote_date=today + timedelta(days=1), quote_type='usd')
        print "Brent quotes already exist today"
    except Quote.DoesNotExist:
        usd_quote_value = getUSDQuotesOnDate(str(today+timedelta(days=1)))
        usd_q = Quote(quote_date=today + timedelta(days=1), quote_value=usd_quote_value, quote_type='usd')
        usd_q.save()
    print "Update has completed"


@periodic_task(run_every=crontab(minute=10, hour=10))
def makeAutomatePrediction():
    net_qs = NeuralNet.objects.all()
    count_usd_quotes = 4
    count_oil_quotes = 2
    today = now().date()
    quotes_qs = []
    if len(net_qs) == 0:
        print "No neironets for prediction"
    for net in net_qs:
        try:
            print net.name
            loaded_net = loadNet(net.neironet_file)
            if Quote.objects.filter(quote_date=today):
                prediction_date = today
            else:
                prediction_date = today - timedelta(days=1)
            if len(Prediction.objects.filter(neiro_net=net, prediction_date__gte=today, prediction_is_automate='Y')) == 0:
                quotes_qs = Quote.objects.filter(quote_date__gt=prediction_date - timedelta(days=count_usd_quotes),
                                                 quote_date__lte=prediction_date, quote_type='usd') | \
                            Quote.objects.filter(quote_date__gt=prediction_date - timedelta(days=count_oil_quotes),
                                                 quote_date__lte=prediction_date, quote_type='brent')
                if len(quotes_qs) == net.number_of_inputs:
                    quotes_list = []
                    for quote in quotes_qs.order_by('-quote_type', 'quote_date'):
                        quotes_list.append(quote.quote_value)
                    prediction_result = loaded_net.activate(quotes_list)[0]
                    print prediction_result
                    data_string = ", ".join(map(str, quotes_list))

                    pred = Prediction(neiro_net=net, input_data=data_string, output_data=prediction_result,
                          predicted_on_date=prediction_date+timedelta(days=1), prediction_is_automate='Y')
                    pred.save()
                else:
                    print "Not enough parameters for prediction"
            else:
                print "Today automatic prediction already exist"
        except IOError:
            print "Neironet file is not exist"



