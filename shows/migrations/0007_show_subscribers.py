# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-08 05:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0006_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='subscribers',
            field=models.ManyToManyField(to='shows.User'),
        ),
    ]
