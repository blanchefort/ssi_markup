# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from apps.home.models import Dialogs, LabelledSSI


admin.site.register(Dialogs)
admin.site.register(LabelledSSI)
