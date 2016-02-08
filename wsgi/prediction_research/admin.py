# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import NeuralNet, Quote, Training, TrainingResult, DataSet, Prediction


class NeiroNetAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'training_epochs')


class QuotesAdmin(admin.ModelAdmin):
    list_display = ('quote_date', 'quote_value', 'quote_type')


class DataSetsAdmin(admin.ModelAdmin):
    list_display = ('data_set_on_date', 'input_data', 'output_data')


class PredictionAdmin(admin.ModelAdmin):
    list_display = ('neiro_net', 'input_data', 'output_data', 'prediction_date', 'predicted_on_date', 'prediction_is_automate')

# Register your models here.
admin.site.register(NeuralNet, NeiroNetAdmin)
admin.site.register(Training)
admin.site.register(TrainingResult)
admin.site.register(Quote, QuotesAdmin)
admin.site.register(DataSet, DataSetsAdmin)
admin.site.register(Prediction, PredictionAdmin)