# -*- encoding: utf-8 -*-
 

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    #path('plot/', views.plot_csv, name='plot_csv'),

    # The home page
    path('', views.index, name='home'),

    path('wendler.html', views.wendler_view, name='wendler'),

    path('export/', views.some_view, name='exporty'),

    path('export_docx/', views.word_doc_view, name='exportie'),

    path('wendler-plans/', views.wendler_plan_list, name='wendler_plan_list'),

    path('wendler-plans/update/<int:plan_id>/', views.update_wendler_plan, name='update_wendler_plan'),

    path('wendler-plans/delete/<int:plan_id>/', views.delete_wendler_plan, name='delete_wendler_plan'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
