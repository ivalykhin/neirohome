# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-02 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_research', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neironet',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
