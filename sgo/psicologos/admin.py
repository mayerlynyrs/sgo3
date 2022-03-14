from django.contrib import admin
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
#Models
from psicologos.models import  Psicologico, PsicologicoTipo, EvaluacionPsicologico , Agenda
from examenes.models import Examen, Evaluacion
# Utils Model
from utils.models import Planta
# Requerimientos
from requerimientos.models import RequerimientoUser
#User
from users.models import User


class PsicologicoSetResource(resources.ModelResource):
    requerimiento_user = fields.Field(column_name='requerimiento_user', attribute='requerimiento_user', widget=ForeignKeyWidget(RequerimientoUser, 'nombre'))
    examen = fields.Field(column_name='examen', attribute='examen', widget=ForeignKeyWidget(Examen, 'nombre'))
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))

    class Meta:
        model = Psicologico
        fields = ('id', 'fecha_inicio', 'fecha_termino', 'estado', 'resultado', 'requerimiento_user', 'examen',
                  'user', 'planta', 'status', )


class PsicologicoTipoSetResource(resources.ModelResource):

    class Meta:
        model = PsicologicoTipo
        fields = ('id', 'nombre', 'status', )


class EvaluacionPsicologicoSetResource(resources.ModelResource):
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'nombre'))
    psicologico_tipo = fields.Field(column_name='psicologico_tipo', attribute='psicologico_tipo', widget=ForeignKeyWidget(PsicologicoTipo, 'nombre'))

    class Meta:
        model = EvaluacionPsicologico
        fields = ('id', 'estado', 'fecha_inicio', 'fecha_termino', 'resultado', 'archivo',
                  'user', 'psicologico_tipo', 'status', )

class AgendaSetResource(resources.ModelResource):
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))

    class Meta:
        model = Agenda
        fields = ('id', 'tipo', 'referido', 'Hal2', 'fecha_ingreso_estimada', 'fecha_agenda_evaluacion', 'estado', 'status', )


@admin.register(Psicologico)
class PsicologicoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """PsicologicoAdmin model admin."""

    resource_class = PsicologicoSetResource
    fields = ('fecha_inicio', 'fecha_termino', 'estado', 'resultado', 'requerimiento_user', 'examen', 'user',
              'planta', 'status' )
    list_display = ('id', 'estado', 'requerimiento_user', 'planta', 'status', 'created_date',)
    list_filter = ['requerimiento_user', 'examen', 'user', 'planta', ]
    search_fields = ['requerimiento_user__nombre', 'examen__nombre', 'user', 'planta__nombre', ]


@admin.register(PsicologicoTipo)
class PsicologicoTipoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """PsicologicoTipoAdmin model admin."""

    resource_class = PsicologicoTipoSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(EvaluacionPsicologico)
class EvaluacionPsicologicoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """EvaluacionPsicologicoAdmin model admin."""

    resource_class = EvaluacionPsicologicoSetResource
    fields = ('estado', 'fecha_inicio', 'fecha_termino', 'resultado', 'archivo',
              'user', 'psicologico_tipo', 'status', )
    list_display = ('id', 'estado', 'fecha_inicio', 'fecha_termino', 'resultado', 'archivo',
                    'user', 'psicologico_tipo', 'status', 'created_date',)
    list_filter = ['estado', 'user', 'psicologico_tipo', ]
    search_fields = ['user__nombre', 'psicologico_tipo__nombre', ]

@admin.register(Agenda)
class AgendaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """AgendaAdmin model admin."""

    resource_class = AgendaSetResource
    fields = ('tipo', 'referido', 'Hal2', 'fecha_ingreso_estimada', 'fecha_agenda_evaluacion', 'estado','obs',
              'user', 'status', )
    list_display = ('tipo', 'referido', 'Hal2', 'fecha_ingreso_estimada', 'fecha_agenda_evaluacion', 'estado','obs',
                    'user', 'status',)
    list_filter = [ 'estado', 'user', ]
    search_fields = [ 'user__nombre', 'evaluacion__nombre', ]
