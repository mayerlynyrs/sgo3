"""Ps urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from psicologos import views


urlpatterns = [
    # Management
    path(
        route='',
        view=views.PsicologosCalendarioView.as_view(),
        name='listAgenda'
     ),
    path(
        route='create',
        view=views.AgendaCreateView.as_view(),
        name='create'
     ),
    path(
        route='list',
        view=views.AgendaList.as_view(),
        name='list'
     ),
    path(
        route='evaTerminadas',
        view=views.EvalTerminadasView.as_view(),
        name='evaTerminadas'
     ),
     
     
    
]