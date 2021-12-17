"""Utils urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from utils import views


urlpatterns = [
    path(
        route='list_area',
        view=views.AreaListView.as_view(),
        name='list_area'
    ),
    path(
        route='create_area',
        view=views.create_area,
        name="create_area"
    ),

    path(
        route='list_cargo',
        view=views.CargoListView.as_view(),
        name='list_cargo'
    ),

    path(
        route='create_cargo',
        view=views.create_cargo,
        name='create_cargo'
    ),

    path(
    route='list_horario',
    view=views.HorarioListView.as_view(),
    name='list_horario'
    ),

    path(
        route='create_horario',
        view=views.create_horario,
        name='create_horario'
    ),
]
