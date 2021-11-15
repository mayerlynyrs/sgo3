"""Ficheros urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from ficheros import views


urlpatterns = [
    # Management
    path(
        route='',
        view=views.FicheroListView.as_view(),
        name='list'
     ),
    path(
        route='<int:planta_id>/',
        view=views.FicheroListView.as_view(),
        name='list'
    ),
    path(
        route='<int:fichero_id>/update/',
        view=views.update_fichero,
        name="update"
    ),
    path(
        route='create',
        view=views.create_fichero,
        name="create"
    ),
    path(
        route='<int:fichero_id>/detail/',
        view=views.detail_fichero,
        name="detail"
    ),
    path(
        route='<int:object_id>/delete/',
        view=views.delete_fichero,
        name="delete"
    ),
]
