"""Ps urls."""

# Django
from django import views
from django.urls import path
from django.contrib.auth import views as auth_views
from consultas import views



urlpatterns = [
    # Management
    path(
        route='consulta_requerimiento',
        view=views.ConsultaRequerimientoView.as_view(),
        name='consulta_requerimiento'
     ),
     path('ajax/load-plantas/', views.load_plantas, name='ajax_load_plantas'), # AJAX
     path('buscarRequerimiento', views.buscar_requerimiento),
      
    
]