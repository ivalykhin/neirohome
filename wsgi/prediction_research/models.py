# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from nets.netManagement import loadNet
from datetime import timedelta
from django.db import models


# Create your models here.
class NeuralNet(models.Model):
    name = models.CharField(max_length=256)
    number_of_inputs = models.IntegerField(default=6)
    number_of_outputs = models.IntegerField(default=1)
    training_epochs = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    neuronet_file = models.CharField(max_length=512, blank=True, null=True)
    description = models.TextField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name

    def makePrediction(self, input_data_list, predicted_on_date, is_auto):
        loaded_net = loadNet(self.neuronet_file)
        prediction_result = loaded_net.activate(input_data_list)[0]
        input_data_string = ", ".join(map(str, input_data_list))
        pred = Prediction(neiro_net=self, input_data=input_data_string, output_data=prediction_result,
                          predicted_on_date=predicted_on_date, prediction_is_automate=is_auto)
        pred.save()


class DataSet(models.Model):
    data_set_on_date = models.DateField()
    input_data = models.CharField(max_length=512)
    output_data = models.DecimalField(max_digits=8, decimal_places=4)
    creation_date = models.DateTimeField(auto_now_add=True)

    def getInputDataList(self):
        return self.input_data.split(',')

    def setDataFromList(self, data_list):
        return ", ".join(map(str, data_list))

    def updateDataSetFromQuotes(self, date):
        pattern = {'inputData': [
                        {'quoteType': 'usd', 'dateDelta': -4},
                        {'quoteType': 'usd', 'dateDelta': -3},
                        {'quoteType': 'usd', 'dateDelta': -2},
                        {'quoteType': 'usd', 'dateDelta': -1},
                        {'quoteType': 'brent', 'dateDelta': -2},
                        {'quoteType': 'brent', 'dateDelta': -1}
                                ],
                    'outputData': [
                        {'quoteType': 'usd', 'dateDelta': 0}
                                ]
                 }
        input_list = []
        output_list = []
        for key in pattern:
            for suite in pattern[key]:
                try:
                    quote = Quote.objects.get(quote_date=date + timedelta(days=suite['dateDelta']),
                                              quote_type=suite['quoteType'])
                    if key == 'inputData':
                        input_list.append(quote.quote_value)
                    elif key == 'outputData':
                        output_list.append(quote.quote_value)
                    else:
                        print "Wrong pattern. Unknown key {0}!".format(key)
                    self.input_data = self.setDataFromList(input_list)
                    self.output_data = self.setDataFromList(output_list)
                    self.data_set_on_date = date
                except Quote.DoesNotExist:
                    print "No quotes for {0} on {1}".format(suite['quoteType'], date+timedelta(days=suite['dateDelta']))


class Quote(models.Model):
    TYPE_CHOICES = (
        ('usd', 'USD'),
        ('brent', 'Brent'),
    )
    quote_date = models.DateField()
    quote_value = models.DecimalField(max_digits=8, decimal_places=4)
    quote_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    creation_date = models.DateTimeField(auto_now_add=True)


class Training(models.Model):
    neural_net = models.ForeignKey(NeuralNet)
    training_data_file = models.CharField(max_length=512)
    training_start_time = models.DateTimeField(auto_now_add=True)
    training_end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.neural_net.name + ' at ' + self.training_start_time.strftime('%d.%m.%Y %H:%M')


class TrainingResult(models.Model):
    training = models.ForeignKey(Training)
    training_epochs = models.IntegerField()
    errors = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.training.__str__() + ' for ' + str(self.training_epochs) + ' epochs with total error: ' \
               + str(self.errors)


class Prediction(models.Model):
    neural_net = models.ForeignKey(NeuralNet)
    number_of_inputs = models.IntegerField(default=6)
    number_of_outputs = models.IntegerField(default=1)
    input_data = models.CharField(max_length=512)
    output_data = models.DecimalField(max_digits=7, decimal_places=4)
    prediction_date = models.DateTimeField(auto_now_add=True)
    predicted_on_date = models.DateField()
    prediction_is_automate = models.CharField(max_length=1, default='N')


class NetStructure(models.Model):
    number_of_layers = models.IntegerField(default=10)
    number_of_neurons_list = models.CharField(max_length=128)
