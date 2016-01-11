# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import NeiroNet


class NeiroNetAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'training_epochs')

# Register your models here.
admin.site.register(NeiroNet, NeiroNetAdmin)
