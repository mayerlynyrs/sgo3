"""Firmas Admin."""
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

# Register your models here.
from firmas.models import EstadoFirma, Firma

class EstadoFirmaSetResource(resources.ModelResource):

    class Meta:
        model = EstadoFirma
        fields = ('id', 'nombre','status', )


class FirmaSetResource(resources.ModelResource):
    estado_firma = fields.Field(column_name='estado_firma', attribute='estado_firma', widget=ForeignKeyWidget(EstadoFirma, 'nombre'))
    class Meta:
        model = Firma
        fields = ('id', 'rut_trabajador', 'estado_firma', 'fecha_firma' , 'respuesta_api', 'status', )


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
    fields = ('respuesta_api', 'rut_trabajador', 'estado_firma', 'fecha_firma',  )
    list_display = ('id', 'rut_trabajador', 'estado_firma', 'fecha_envio', 'fecha_firma', 'respuesta_api',)
    search_fields = ['respuesta_api', 'rut_trabajador', 'estado_firma', 'fecha_envio', 'fecha_firma', ]
