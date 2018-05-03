from __future__ import absolute_import
# -*- coding:utf-8 -*-
__author__ = 'SRP'
__date__ = '2018/4/25 13:48'

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','Mxonline362.settings')
django.setup()

app = Celery('Mxonline362')
# app = Celery('utils.email_send',broker=settings.BROKER_URL)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)