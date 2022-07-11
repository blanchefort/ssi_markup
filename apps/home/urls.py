# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    # markup
    path('markup', views.markup, name='markup'),
    # rules
    path('rules', views.rules, name='rules'),
    # upload
    path('upload', views.upload, name='upload'),
    # download
    path('download', views.download, name='download'),

]
