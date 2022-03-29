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
from requerimientos.models import RequerimientoUser
#User
from users.models import User


class ExamenSetResource(resources.ModelResource):

    class Meta:
        model = Examen
        fields = ('id', 'nombre', 'valor', 'status', )


class BateriaSetResource(resources.ModelResource):
    examen = fields.Field(column_name='examen', attribute='examen',widget=ManyToManyWidget(Examen, ',', 'pk'))

    class Meta:
        model = Bateria
        fields = ('id', 'nombre', 'status', )


class EvaluacionSetResource(resources.ModelResource):
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'nombre'))
    examen = fields.Field(column_name='examen', attribute='examen', widget=ForeignKeyWidget(Examen, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))

    class Meta:
        model = Evaluacion
        fields = ('id', 'nombre', 'fecha_examen', 'fecha_vigencia', 'descripcion', 'valor_examen', 'referido', 'resultado',
                  'archivo', 'user', 'examen', 'planta', 'status', )


class RequerimientoSetResource(resources.ModelResource):
    requerimiento_user = fields.Field(column_name='requerimiento_user', attribute='requerimiento_user', widget=ForeignKeyWidget(RequerimientoUser, 'nombre'))
    examen = fields.Field(column_name='examen', attribute='examen', widget=ForeignKeyWidget(Examen, 'nombre'))
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))

    class Meta:
        model = Requerimiento
        fields = ('id', 'fecha_inicio', 'fecha_termino', 'estado', 'resultado', 'requerimiento_user', 'examen',
                  'user', 'planta', 'status', )



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


@admin.register(Evaluacion)
class EvaluacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """EvaluacionAdmin model admin."""

    resource_class = EvaluacionSetResource
    fields = ('nombre', 'fecha_examen', 'fecha_vigencia', 'descripcion', 'valor_examen', 'referido', 'resultado',
              'archivo', 'user', 'examen', 'planta', 'status', )
    list_display = ('id', 'nombre', 'fecha_examen', 'user', 'status', 'modified',)
    list_filter = ['user', 'examen', 'planta', ]
    search_fields = ['user__nombre', 'examen__nombre', 'planta__nombre', ]


@admin.register(Requerimiento)
class RequerimientoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """RequerimientoAdmin model admin."""

    resource_class = RequerimientoSetResource
    fields = ('fecha_inicio', 'fecha_termino', 'estado', 'resultado', 'requerimiento_user', 'examen', 'user',
              'planta', 'status' )
    list_display = ('id', 'estado', 'requerimiento_user', 'planta', 'status', 'modified',)
    list_filter = ['requerimiento_user', 'examen', 'user', 'planta', ]
    search_fields = ['requerimiento_user__nombre', 'examen__nombre', 'user', 'planta__nombre', ]