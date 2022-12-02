"""Ps urls."""

# Django
from django import views
from django.urls import path
from django.contrib.auth import views as auth_views
from consultas import views



urlpatterns = [
    # Management
    path(
        route='',
        view=views.ConsultaRequerimientoView.as_view(),
        name='list'
     ),
    path('ajax/load-plantas/', views.load_plantas, name='ajax_load_plantas'), # AJAX
    path('buscarRequerimiento', views.buscar_requerimiento),
    path(
        route='epps',
        view=views.ConsultaEppView.as_view(),
        name='epps'
     ),
    path('ajax/load-areas-cargos/', views.load_areas_cargos, name='ajax_load_areas_cargos'), # AJAX
    path('buscarRequerimientoAC', views.buscar_requerimiento_ac),
    path(
        route='requerimiento_epps',
        view=views.RequerimientoEppView.as_view(),
        name='requerimiento-epps'
     ),
    path('buscarRequerimientoEpp', views.buscar_epps_requerimiento),
    path(
        route='create',
        view=views.ConvenioClienteView.as_view(),
        name='create'
     ),
    path('buscarConvenioCliente', views.buscar_convenio_cliente),
      
    
]