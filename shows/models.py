'''models.py - Contains the Show model and the YesterdayID model.'''
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

class Show(models.Model):
    '''Show is a model that contains the name of the show, the show_id,
    the subscribers to the show, and the next known airdate of the show.'''
    name = models.CharField(max_length=200)
    show_id = models.IntegerField()
    subscribers = models.ManyToManyField(User)
    date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.name

class YesterdayID(models.Model):
    '''YesterdayID contains the show ids used in syncdaily5.py that were in
    the TV schedule from yesterday.'''
    show_id = models.IntegerField()
    def __str__(self):
        return self.show_id