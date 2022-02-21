"""Requerimientos urls."""

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
        route='<int:planta_id>/',
        view=views.RequerimientoListView.as_view(),
        name='list'
    ),
    path(
        route='<int:requerimiento_id>/update/',
        view=views.update_requerimiento,
        name="update"
    ),
    path(
        route='<int:requerimiento_id>/create_requerimiento',
        view=views.RequerimientoIdView.as_view(),
        name='create_requerimiento'
    ),
    path(
        route='create',
        view=views.create_requerimiento,
        name="create"
    ),
    path(
        route='<int:requerimiento_id>/detail/',
        view=views.detail_requerimiento,
        name="detail"
    ),
    path(
        route='<int:requerimiento_id>/acr/',
        view=views.ACRView.as_view(),
        name='acr'
     ),
    path(
        route='<int:requerimiento_id>/requirement_users/',
        view=views.RequirementUserView.as_view(),
        name='requirement_users'
     ),
    path(
        route='<int:object_id>/delete/',
        view=views.delete_requerimiento,
        name="delete"
    ),
    
    
    path('ajax/load-plantas/', views.load_plantas, name='ajax_load_plantas'), # AJAX
]
