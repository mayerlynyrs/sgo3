"""Utils urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from utils import views


urlpatterns = [
    path(
        route='area',
        view=views.AreaView.as_view(),
        name='area'
    ),
    path(
        route='cargo',
        view=views.CargoView.as_view(),
        name='cargo'
    ),
    path(
        route='horario',
        view=views.HorarioView.as_view(),
        name='horario'
    ),
    path(
        route='bono',
        view=views.BonoView.as_view(),
        name='bono'
    ),
    path(
        route='salud',
        view=views.SaludView.as_view(),
        name='salud'
    ),
    path(
        route='afp',
        view=views.AfpView.as_view(),
        name='afp'
    ),
    path(
        route='valores_diarios',
        view=views.ValoresDiarioView.as_view(),
        name='valores_diarios'
    ),
    path(
        route='vdiarios_afp',
        view=views.ValoresDiarioAfpView.as_view(),
        name='vdiarios_afp'
    ),
]
