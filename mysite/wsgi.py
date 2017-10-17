"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

"""

import os
import sys

path = '/home/tvshowpremieredate/mysite'
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
