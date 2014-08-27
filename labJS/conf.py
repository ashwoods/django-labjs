# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from appconf import AppConf
from django.conf import settings  # noqa


class LabjsConf(AppConf):

    ENABLED = not settings.DEBUG
    DEBUG_TOGGLE = 'labjs'
