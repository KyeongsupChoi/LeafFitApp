# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('wendler.html', views.wendler_view, name='wendler'),

    path('export/', views.some_view, name='exporty'),

    path('export_doc/', views.word_doc_view, name='exportie'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
