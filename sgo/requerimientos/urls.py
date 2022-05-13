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
        route='<int:object_id>/delete/',
        view=views.delete_requerimiento,
        name="delete"
    ),
    path(
        route='<int:requerimiento_id>/acr/',
        view=views.ACRView.as_view(),
        name='acr'
     ),
    path(
        route='<int:requerimiento_id>/requirement_trabajadores/',
        view=views.RequirementTrabajadorView.as_view(),
        name='requirement_trabajadores'
     ),
    path(
        route='<int:requerimiento_id>/adendum/',
        view=views.adendum_requerimiento,
        name="adendum"
    ),
    path(
        route='create_adendum',
        view=views.create_adendum,
        name="create_adendum"
    ),
    path(
        route='<int:requerimiento_id>/apd/',
        view=views.a_puesta_disposicion,
        name="apd"
    ),
    path(
        route='<int:adendum_id>/descargar_adendum/',
        view=views.descargar_adendum,
        name="descargar_adendum"
    ),
    
    
    path('ajax/load-plantas/', views.load_plantas, name='ajax_load_plantas'), # AJAX
]
