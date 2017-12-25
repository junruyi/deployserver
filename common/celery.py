from __future__ import  absolute_import, unicode_literals
import  os
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','deployserver.settings')

from django.conf   import settings

app = Celery('deployserver')
app.config_from_object('django.conf:settings')
app.autodiscover_task(lambda :[app_config.split('.')[0]
                               for app_config in settings.INSTALLED_APPS])
