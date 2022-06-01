"""Agendamientos urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from agendamientos import views


urlpatterns = [
    # Management
    path(
        route='listAgenda',
        view=views.AgendaCalendarioView.as_view(),
        name='listAgenda'
     ),
    path(
        route='create',
        view=views.AgendaCreateView.as_view(),
        name='create'
     ),
    path(
        route='solicitudes',
        view=views.SolicitudesUserView.as_view(),
        name='solicitudes'
     )  
] 