# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-06 23:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0003_show'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='show',
            name='premiere',
        ),
    ]