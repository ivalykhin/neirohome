# -*- coding: utf-8 -*-
from celery.task import periodic_task
from celery.schedules import crontab
from datetime import timedelta, datetime, date
from .models import NeiroNet, DataSets, Training, TrainingResult
from nets.netManagement import createAndTrainNetworkFromList
from nets.getQuotesData import getCurrentOilQuotes, getUSDQuotesOnDate


@periodic_task(run_every=timedelta(minutes=2))
def createAndTrainNet():
    try:
        net_info = NeiroNet.objects.filter(training_epochs=0).order_by('-creation_date')[0]
    except IndexError:
        print "All networks are trained"
        net_info = []
    if net_info:
        print "Start trainig"
        training = Training(training_data_file='FromDB')
        training.neiro_net_id = net_info
        training.save()
        net_info.training_epochs = 1
        net_info.save()
        dataset_list = DataSets.objects.order_by('-data_set_on_date')[::-1]
        train_list = []
        for i in range(0, len(dataset_list)):
            temp_list = dataset_list[i].input_data.split(',')
            temp_list.append(str(dataset_list[i].output_data))
            train_list.append(temp_list)
        try:
            train_results = createAndTrainNetworkFromList(train_list, net_info.number_of_inputs, net_info.name+'.xml', max_epochs=2550)
            net_info.neironet_file = train_results[1]
            net_info.training_epochs += len(train_results[0][0])-3
            training.training_end_time = datetime.now()
            training_result = TrainingResult(training_epochs=len(train_results[0][1]), errors=train_results[0][0][-1])-3
            training_result.training_id = training
            net_info.save()
            training.save()
            training_result.save()
        except Exception as detail:
            print "Error: ", detail
            net_info.training_epochs = 0
            net_info.save()
            training.delete()


@periodic_task(run_every=crontab(minute=0, hour=17))
def todayQuotesToDataSet(count_usd_quotes=4, count_oil_quotes=2):
    today = date.today()
    try:
        today_datset = DataSets.objects.filter(data_set_on_date=today)[0]
        print "Today dataset already exist: " + today_datset.input_data
    except IndexError:
        print "Today dataset is absent. Generating..."
        try:
            data_set = DataSets.objects.filter(data_set_on_date=today-timedelta(days=1))[0]
        except IndexError:
            print "Yesterday dataset is absent. Validate datasets manual."
            data_set = []
        if data_set:
            usd_quote = getUSDQuotesOnDate(today.__str__())
            oil_quotes = getCurrentOilQuotes()
            try:
                data_set_input_list = data_set.input_data.split(', ')
                for i in range(0, len(data_set_input_list)):
                    if i < count_usd_quotes - 1:
                        data_set_input_list[i] = data_set_input_list[i+1]
                    elif i == count_usd_quotes - 1:
                        data_set_input_list[i] = data_set.output_data
                    elif (i > count_usd_quotes - 1) and (i < count_usd_quotes + count_oil_quotes - 1):
                        data_set_input_list[i] = data_set_input_list[i+1]
                    else:
                        data_set_input_list[i] = oil_quotes
                input_data = ""
                for i in range(0, len(data_set_input_list)):
                    input_data += str(data_set_input_list[i]) + ', '
                data_set_new = DataSets(data_set_on_date=today, input_data=input_data[:-2], output_data=usd_quote)
                data_set_new.save()
            except Exception as detail:
                print "Error: ", detail