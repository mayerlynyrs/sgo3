"""Examenes urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from requerimientos import views


urlpatterns = [
    # Management
    path(
        route='',
        view=views.RequerimientoListView.as_view(),
        name='list'
     ),
    path(
        route='create',
        view=views.create_requerimiento,
        name="create"
    ),
]
