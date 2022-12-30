"""Firmas Admin."""
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

# Register your models here.
from firmas.models import EstadoFirma, Firma
from contratos.models import Contrato, TipoDocumento
from requerimientos.models import PuestaDisposicion 
from users.models import Trabajador

class EstadoFirmaSetResource(resources.ModelResource):

    class Meta:
        model = EstadoFirma
        fields = ('id', 'nombre','status', )


class FirmaSetResource(resources.ModelResource):
    estado_firma = fields.Field(column_name='estado_firma', attribute='estado_firma', widget=ForeignKeyWidget(EstadoFirma, 'nombre'))
    contrato = fields.Field(column_name='contrato', attribute='contrato', widget=ForeignKeyWidget(Contrato, 'nombre'))
    trabajador = fields.Field(column_name='trabajador', attribute='trabajador', widget=ForeignKeyWidget(Trabajador, 'first_name'))
    apd = fields.Field(column_name='apd', attribute='apd', widget=ForeignKeyWidget(PuestaDisposicion, 'codigo_pd'))
    tipo_documento = fields.Field(column_name='tipo_documento', attribute='tipo_documento', widget=ForeignKeyWidget(TipoDocumento, 'nombre'))
    class Meta:
        model = Firma
        fields = ('id', 'rut_trabajador', 'fecha_firma', 'estado_firma', 'respuesta_api', 'status', )


@admin.register(EstadoFirma)
class EstadoFirmaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """EstadoFirmaAdmin model admin."""

    resource_class = EstadoFirmaSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created',)
    search_fields = ['nombre', ]


@admin.register(Firma)
class FirmaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """FirmaAdmin model admin."""

    resource_class = FirmaSetResource
    fields = ('respuesta_api', 'rut_trabajador', 'estado_firma', 'fecha_firma', 'contrato', 'trabajador', 'apd', 'tipo_documento', 'status')
    list_display = ('id', 'rut_trabajador', 'estado_firma', 'fecha_envio', 'fecha_firma', 'respuesta_api',)
    search_fields = ['respuesta_api', 'rut_trabajador', 'estado_firma', 'fecha_envio', 'fecha_firma', ]
