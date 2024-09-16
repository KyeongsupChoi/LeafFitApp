# -*- encoding: utf-8 -*-
 

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    #path('plot/', views.plot_csv, name='plot_csv'),

    # The home page
    path('', views.index, name='home'),

    path('wendler.html', views.wendler_view, name='wendler'),

    path('export_pdf/', views.some_view, name='exporty'),

    path('export_docx/', views.word_doc_view, name='exportie'),



    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
