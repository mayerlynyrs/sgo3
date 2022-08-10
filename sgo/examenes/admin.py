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
from examenes.models import Examen, Bateria, CentroMedico, Evaluacion, Requerimiento
# Clientes
from clientes.models import Planta
# Requerimientos
from requerimientos.models import RequerimientoTrabajador
#trabajador
from users.models import User, Trabajador
from utils.models import Cargo


class ExamenSetResource(resources.ModelResource):

    class Meta:
        model = Examen
        fields = ('id', 'nombre', 'valor', 'status', )


class BateriaSetResource(resources.ModelResource):
    examen = fields.Field(column_name='examen', attribute='examen',widget=ManyToManyWidget(Examen, ',', 'pk'))

    class Meta:
        model = Bateria
        fields = ('id', 'nombre', 'status', )


class CentroMedicoSetResource(resources.ModelResource):

    class Meta:
        model = CentroMedico
        fields = ('id', 'nombre', 'region', 'provincia', 'ciudad', 'direccion', 'status', )


class EvaluacionSetResource(resources.ModelResource):
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))
    trabajador = fields.Field(column_name='trabajador', attribute='trabajador', widget=ForeignKeyWidget(Trabajador, 'nombre'))
    bateria = fields.Field(column_name='bateria', attribute='bateria', widget=ForeignKeyWidget(Bateria, 'nombre'))
    cargo = fields.Field(column_name='cargo', attribute='cargo', widget=ForeignKeyWidget(Cargo, 'nombre'))
    centro = fields.Field(column_name='centro', attribute='centro',widget=ForeignKeyWidget(CentroMedico, 'nombre'))
    psicologo = fields.Field(column_name='psicologo', attribute='psicologo', widget=ForeignKeyWidget(User, 'first_name'))

    class Meta:
        model = Evaluacion
        fields = ('id', 'fecha_inicio', 'fecha_termino', 'referido', 'resultado', 'archivo', 'archivo2', 'planta_id', 'trabajador_id', 'bateria_id', 'cargo_id', 'centro_id', 'estado', 'hal2', 'psicologo_id', 'tipo', 'tipo_evaluacion', 'valor', 'status', )


class RequerimientoSetResource(resources.ModelResource):
    requerimiento_trabajador = fields.Field(column_name='requerimiento_trabajador', attribute='requerimiento_trabajador', widget=ForeignKeyWidget(RequerimientoTrabajador, 'nombre'))
    bateria = fields.Field(column_name='bateria', attribute='bateria', widget=ForeignKeyWidget(Bateria, 'nombre'))
    trabajador = fields.Field(column_name='trabajador', attribute='trabajador', widget=ForeignKeyWidget(Trabajador, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))

    class Meta:
        model = Requerimiento
        fields = ('id', 'estado', 'requerimiento_trabajador', 'bateria', 'psicologico', 'hal2', 'trabajador', 'planta', 'obs', 'status', )



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


@admin.register(CentroMedico)
class CentroMedicoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """CentroMedicoAdmin model admin."""

    resource_class = CentroMedicoSetResource
    fields = ('nombre', 'region', 'provincia', 'ciudad', 'direccion', 'status', )
    list_display = ('id', 'nombre', 'region', 'provincia', 'ciudad', 'direccion', 'status',)
    search_fields = ['nombre', 'region', ]


@admin.register(Evaluacion)
class EvaluacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """EvaluacionAdmin model admin."""

    resource_class = EvaluacionSetResource
    fields = ('fecha_inicio', 'fecha_termino', 'referido', 'resultado', 'archivo', 'archivo2', 'planta', 'trabajador', 'bateria', 'cargo', 'centro', 'estado', 'hal2', 'psicologo', 'tipo', 'tipo_evaluacion', 'valor', )
    list_display = ('id', 'estado', 'archivo', 'planta', 'trabajador', 'bateria', 'resultado', 'hal2', 'psicologo', 'valor', 'status', 'created_date',)
    search_fields = ['trabajador__nombre', 'bateria__nombre', 'trabajador', 'planta__nombre', ]


@admin.register(Requerimiento)
class RequerimientoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """RequerimientoAdmin model admin."""

    resource_class = RequerimientoSetResource
    fields = ('estado', 'requerimiento_trabajador', 'bateria', 'psicologico', 'hal2', 'trabajador', 'planta', 'obs', 'status' )
    list_display = ('id', 'estado', 'requerimiento_trabajador', 'planta', 'status', 'modified',)
    list_filter = ['requerimiento_trabajador', 'bateria', 'trabajador', 'planta', ]
    search_fields = ['requerimiento_trabajador__nombre', 'bateria__nombre', 'trabajador', 'planta__nombre', ]