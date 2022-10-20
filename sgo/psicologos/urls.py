"""Psicologos urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from psicologos import views


urlpatterns = [
    # Management
    path(
        route='',
        view=views.PsicologosCalendarioView.as_view(),
        name='listAgenda'
     ),
    path(
        route='create',
        view=views.AgendaCreateView.as_view(),
        name='create'
     ),
    path(
        route='list',
        view=views.AgendaList.as_view(),
        name='list'
     ),
    path(
        route='evalu_terminadas',
        view=views.EvalTerminadasView.as_view(),
        name='evalu-terminadas'
     ),
    path(
        route='list_solicitudes',
        view=views.PsiSolicitudesList.as_view(),
        name='list-solicitudes'
     ),
    path(
        route='<int:requerimiento_id>/revision/',
        view=views.revision_solicitudes,
        name="revision"
    ),
    path(
        route='<int:trabajador_id>/examenes/',
        view=views.examenes_trabajador,
        name="examenes"
    ),
    path(
        route='<int:evaluacion_id>/documento/',
        view=views.documento_trabajador,
        name="documento"
    ),
    
]