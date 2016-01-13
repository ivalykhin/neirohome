# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class NeiroNet(models.Model):
    name = models.CharField(max_length=256)
    number_of_inputs = models.IntegerField(default=6)
    number_of_outputs = models.IntegerField(default=1)
    training_epochs = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    neironet_file = models.CharField(max_length=512, blank=True, null=True)
    description = models.TextField(max_length=1024, blank=True, null=True)


class DataSets(models.Model):
    data_set_on_date = models.DateField()
    input_data = models.CharField(max_length=512)
    output_data = models.DecimalField(max_digits=8, decimal_places=4)


class Training(models.Model):
    neiro_net = models.ForeignKey(NeiroNet)
    training_data_file = models.CharField(max_length=512)
    training_start_time = models.DateTimeField(auto_now_add=True)
    training_end_time = models.DateTimeField(blank=True, null=True)


class TrainingResult(models.Model):
    training = models.ForeignKey(Training)
    training_epochs = models.IntegerField()
    errors = models.DecimalField(max_digits=4, decimal_places=4)


class Prediction(models.Model):
    neiro_net = models.ForeignKey(NeiroNet)
    number_of_inputs = models.IntegerField(default=6)
    number_of_outputs = models.IntegerField(default=1)
    input_data = models.CharField(max_length=512)
    output_data = models.DecimalField(max_digits=4, decimal_places=4)
    prediction_date = models.DateTimeField(auto_now_add=True)
    predicted_on_date = models.DateField()