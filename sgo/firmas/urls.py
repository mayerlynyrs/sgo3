"""Firmas urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from firmas import views


urlpatterns = [
    # Management
    path(
        route='',
        view=views.ContratoAprobadoList.as_view(),
        name='list'
     ),
    # path(
    #     route='<int:planta_id>/',
    #     view=views.FirmaListView.as_view(),
    #     name='list'
    # ),
]
