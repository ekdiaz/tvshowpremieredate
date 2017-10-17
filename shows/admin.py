'''admin.py adds Shows to the admin site.'''
from django.contrib import admin
from .models import Show

admin.site.register(Show)