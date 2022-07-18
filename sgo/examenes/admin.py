"""Requerimientos Admin."""

# Register your models here.

# Django
from django.contrib import admin
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget
#Models
from examenes.models import Examen, Bateria, Evaluacion, Requerimiento
# Clientes
from clientes.models import Planta
# Requerimientos
from requerimientos.models import RequerimientoTrabajador
#trabajador
from users.models import Trabajador


class ExamenSetResource(resources.ModelResource):

    class Meta:
        model = Examen
        fields = ('id', 'nombre', 'valor', 'status', )


class BateriaSetResource(resources.ModelResource):
    examen = fields.Field(column_name='examen', attribute='examen',widget=ManyToManyWidget(Examen, ',', 'pk'))

    class Meta:
        model = Bateria
        fields = ('id', 'nombre', 'status', )




class RequerimientoSetResource(resources.ModelResource):
    requerimiento_trabajador = fields.Field(column_name='requerimiento_trabajador', attribute='requerimiento_trabajador', widget=ForeignKeyWidget(RequerimientoTrabajador, 'nombre'))
    bateria = fields.Field(column_name='bateria', attribute='bateria', widget=ForeignKeyWidget(Bateria, 'nombre'))
    trabajador = fields.Field(column_name='trabajador', attribute='trabajador', widget=ForeignKeyWidget(Trabajador, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))

    class Meta:
        model = Requerimiento
        fields = ('id', 'fecha_inicio', 'fecha_termino', 'fecha_evaluacion', 'estado', 'resultado', 'requerimiento_trabajador', 'bateria',
                  'hal2', 'trabajador', 'planta', 'obs', 'status', )



@admin.register(Examen)
class ExamenAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ExamenAdmin model admin."""

    resource_class = ExamenSetResource
    fields = ('nombre', 'valor', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', 'valor', ]


@admin.register(Bateria)
class BateriaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """BateriaAdmin model admin."""

    resource_class = BateriaSetResource
    fields = ('nombre', 'examen', 'status', )
    list_display = ('id', 'nombre', 'examenes_list', 'status', 'created_date',)
    search_fields = ['nombre', ]

    def examenes_list(self, obj):
        return u", ".join(o.nombre for o in obj.examen.all())




@admin.register(Requerimiento)
class RequerimientoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """RequerimientoAdmin model admin."""

    resource_class = RequerimientoSetResource
    fields = ('fecha_inicio', 'fecha_termino', 'fecha_evaluacion', 'estado', 'resultado', 'requerimiento_trabajador',
             'bateria', 'hal2', 'trabajador', 'planta', 'obs', 'status' )
    list_display = ('id', 'estado', 'requerimiento_trabajador', 'planta', 'status', 'modified',)
    list_filter = ['requerimiento_trabajador', 'bateria', 'trabajador', 'planta', ]
    search_fields = ['requerimiento_trabajador__nombre', 'bateria__nombre', 'trabajador', 'planta__nombre', ]