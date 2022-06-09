"""EPPs urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from epps import views

# Create your views here.


urlpatterns = [
    path(
        route='tipo/list/',
        view=views.TipoListView.as_view(),
        name="list-tipo"
    ),
    path(
        route='insumo',
        view=views.InsumoView.as_view(),
        name='insumo'
    ),
    # path(
    #     route='cargo',
    #     view=views.CargoView.as_view(),
    #     name='cargo'
    # ),
    # path(
    #     route='horario',
    #     view=views.HorarioView.as_view(),
    #     name='horario'
    # ),
    # path(
    #     route='bono',
    #     view=views.BonoView.as_view(),
    #     name='bono'
    # ),
    
]

