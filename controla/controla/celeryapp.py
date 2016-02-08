from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
import os.path
if os.path.isfile('settings/local.py'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'controla.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'controla.settings.production')

app = Celery('controla')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
