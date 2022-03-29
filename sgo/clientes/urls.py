"""Clientes urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from clientes import views


urlpatterns = [
    path(
        route='',
        view=views.ClientListView.as_view(),
        name='list'
     ),
    path(
        route='<int:planta_id>/',
        view=views.ClientListView.as_view(),
        name='list'
    ),
    path(
        route='list_cliente',
        view=views.ClientListView.as_view(),
        name='list_cliente'
    ),
    path(
        route='create_cliente',
        view=views.create_cliente,
        name='create_cliente'
    ),
    path(
        route='<int:cliente_id>/create_cliente',
        view=views.ClienteIdView.as_view(),
        name='create_cliente'
    ),
    path(
        route='<int:cliente_id>/update/',
        view=views.update_cliente,
        name="update"
    ),
    path(
        route='<int:cliente_id>/negocios/',
        view=views.NegocioView.as_view(),
        name='negocios'
     ),
    path(
        route='<int:cliente_id>/plantas/',
        view=views.PlantaView.as_view(),
        name='plantas'
     ),
]