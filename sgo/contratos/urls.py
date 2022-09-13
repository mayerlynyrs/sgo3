"""Contratos urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from contratos import views


urlpatterns = [
    # Plantillas
    path(
        route='plantilla/list/',
        view=views.PlantillaListView.as_view(),
        name="list-plantilla"
    ),
    path(
        route='plantilla/create/',
        view=views.create_plantilla,
        name="create-plantilla"
    ),
    path(
        route='<int:plantilla_id>/plantilla/update/',
        view=views.update_plantilla,
        name="update-plantilla"
    ),
    path(
        route='<int:object_id>/plantilla/delete/',
        view=views.delete_plantilla,
        name="delete-plantilla"
    ),
    # tipo de contratos
    path(
        route='tipo_contratos',
        view=views.TipoContratosView.as_view(),
        name='tipo-contratos'
     ),
    # Requerimiento Contrato
    path(
        route='<int:requerimiento_trabajador_id>/create_contrato/',
        view=views.ContratoIdView.as_view(),
        name="create_contrato"
    ),
    # Contratos
    path(
        route='list/',
        view=views.ContratoListView.as_view(),
        name="list"
    ),
    path(
        route='create/',
        view=views.create,
        name="create"
    ),
    path(
        route='<int:contrato_id>/update_contrato/',
        view=views.update_contrato,
        name="update_contrato"
    ),
    path(
        route='solicitud-contrato/',
        view=views.SolicitudContrato.as_view(),
        name="solicitud-contrato"
    ),
    path(
        route='list_completa',
        view=views.ContratoCompletaListView.as_view(),
        name="list-completa"
    ),
    path('buscarContrato', views.buscar_contrato),
    path(
        route='list_baja_contrato/',
        view=views.BajaContrato.as_view(),
        name="list-baja-contrato"
    ),
    path(
        route='<int:contrato_id>/solicitudes-pendientes/',
        view=views.solicitudes_pendientes,
        name="solicitudes-pendientes"
    ),
    path(
        route='<int:contrato_id>/solicitudes-pendientes-baja/',
        view=views.solicitudes_pendientes_baja,
        name="solicitudes-pendientes-baja"
    ),
    path(
        route='<int:contrato_id>/baja_contrato/',
        view=views.baja_contrato,
        name="baja_contrato"
    ),
    path(
        route='list_baja',
        view=views.ContratoBajaListView.as_view(),
        name="bajadas-contrato"
    ),
    path('buscarBajaContrato', views.buscar_baja_contrato),
    path(
        route='miscontratos/',
        view=views.ContratoMis.as_view(),
        name="miscontratos"
    ),
    path(
        route='<int:pk>/detail/',
        view=views.ContratoDetailView.as_view(),
        name="detail"
    ),
    path(
        route='<int:contrato_id>/enviar_revision_contrato/',
        view=views.enviar_revision_contrato,
        name="enviar_revision_contrato"
    ),
    # Anexos
    path(
        route='anexo/create/',
        view=views.create_anexo,
        name="create-anexo"
    ),
    path(
        route='<int:anexo_id>/update_anexo/',
        view=views.update_anexo,
        name="update_anexo"
    ),
    path(
        route='anexo/solicitud/',
        view=views.SolicitudAnexo.as_view(),
        name="solicitud-anexo"
    ),
    path(
        route='<int:anexo_id>/enviar_revision_anexo/',
        view=views.enviar_revision_anexo,
        name="enviar_revision_anexo"
    ),
    path(
        route='<int:anexo_id>/solicitudes-pendientes-anexo/',
        view=views.solicitudes_pendientes_anexo,
        name="solicitudes-pendientes-anexo"
    ),
    path(
        route='anexo/list_completa',
        view=views.AnexoCompletaListView.as_view(),
        name="list-completa-anexo"
    ),
    path('anexo/buscarAnexo', views.buscar_anexo),
    path(
        route='anexo/list-baja/',
        view=views.BajaAnexo.as_view(),
        name="list-baja-anexo"
    ),
    path(
        route='<int:anexo_id>/baja_contrato_anexo/',
        view=views.baja_contrato_anexo,
        name="baja_contrato_anexo"
    ),
    path(
        route='anexo/list_baja',
        view=views.AnexoBajaListView.as_view(),
        name="bajadas-anexo"
    ),
    path('anexo/buscarBajaAnexo', views.buscar_baja_anexo),
    path(
        route='<int:contrato_id>/generar_firma/',
        view=views.generar_firma_contrato,
        name='generar_firma'
    ),
    path(
        route='<int:id>/firmar/',
        view=views.ContratoFirmarView.as_view(),
        name='firmar'
    ),
    path(
        route='<slug:id>/generar_firma/firmarr/',
        view=auth_views.PasswordResetDoneView.as_view(),
        name='generar_firma_done'
    ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
]
