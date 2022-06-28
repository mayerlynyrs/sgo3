"""Epps Admin."""

from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget

# Register your models here.
# EPP
from epps.models import TipoInsumo, Insumo, Convenio
from clientes.models import Cliente, Planta
# Requerimientos
from requerimientos.models import Requerimiento

class TipoInsumoSetResource(resources.ModelResource):

    class Meta:
        model = TipoInsumo
        fields = ('id', 'nombre', 'status', )


class InsumoSetResource(resources.ModelResource):
    tipo_insumo = fields.Field(column_name='tipo_insumo', attribute='tipo_insumo', widget=ForeignKeyWidget(TipoInsumo, 'nombre'))

    class Meta:
        model = Insumo
        fields = ('id', 'codigo_externo', 'nombre', 'costo', 'tipo_insumo', 'status', )


class ConvenioSetResource(resources.ModelResource):
    insumo = fields.Field(column_name='insumo', attribute='insumo', widget=ManyToManyWidget(Insumo, ',', 'pk'))
    cliente = fields.Field(column_name='cliente', attribute='cliente', widget=ForeignKeyWidget(Cliente, 'razon_social'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))

    model = Convenio
    fields = ('id', 'nomnre', 'valor', 'validez', 'status')


# class AsignacionConvenioSetResource(resources.ModelResource):
#     convenio = fields.Field(column_name='convenio', attribute='convenio', widget=ForeignKeyWidget(Convenio, 'nombre'))
#     requerimiento = fields.Field(column_name='requerimiento', attribute='requerimiento', widget=ForeignKeyWidget(Requerimiento, 'nombre'))

#     model = AsignacionConvenio
#     fields = ('id', 'convenio', 'requerimiento', 'status')


@admin.register(TipoInsumo)
class TipoInsumoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """TipoInsumoAdmin model admin."""

    resource_class = TipoInsumoSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre',)
    search_fields = ['nombre', ]


@admin.register(Insumo)
class InsumoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """InsumoAdmin model admin."""

    resource_class = InsumoSetResource
    fields = ('codigo_externo', 'nombre', 'costo', 'tipo_insumo', 'status', )
    list_display = ('id', 'codigo_externo', 'nombre', 'costo', 'tipo_insumo', 'created_date',)
    search_fields = ['codigo_externo', 'nombre', 'costo', 'tipo_insumo', ]


@admin.register(Convenio)
class Convenio(ImportExportModelAdmin, admin.ModelAdmin):
    """ConvenioAdmnin model Admin."""

    resource_class = ConvenioSetResource
    fields = ('nombre', 'valor', 'validez', 'insumo', 'cliente', 'planta', 'status')
    list_display = ('id', 'nombre', 'valor', 'validez', 'planta', 'created_date')
    search_fields = ('nombre', )


# @admin.register(AsignacionConvenio)
# class AsignacionConvenio(ImportExportModelAdmin, admin.ModelAdmin):
#     """AsignacionConvenioAdmnin model Admin."""

#     fields = ('convenio', 'requerimiento', 'status')
#     list_display = ('id', 'convenio', 'requerimiento', 'created_date')
#     search_fields = ('convenio', 'requerimiento', )
