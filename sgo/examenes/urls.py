"""Examenes urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from examenes import views


urlpatterns = [
    # Management
    path(
        route='examen',
        view=views.ExamenView.as_view(),
        name='examen'
    ),
    path(
        route='bateria',
        view=views.BateriaView.as_view(),
        name='bateria'
    ),
    path(
        route='listEvaluaciones',
        view=views.AgendaList.as_view(),
        name='listEvaluaciones'
    ),
    path(
        route='centroMedico',
        view=views.CentroMedicoView.as_view(),
        name='centroMedico'
    ),
]
