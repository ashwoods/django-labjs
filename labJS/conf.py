import os
from django import VERSION as DJANGO_VERSION
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


class LabjsConf(AppConf):

    # Main switch
    ENABLED = not settings.DEBUG
    DEBUG_TOGGLE = "labjs"
