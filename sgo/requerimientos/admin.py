"""Requerimientos Admin."""

# Register your models here.

# Django
from django.contrib import admin
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.widgets import ManyToManyWidget
from import_export.admin import ImportExportModelAdmin
#Models
from requerimientos.models import Causal, Requerimiento, AreaCargo, RequerimientoUser, Adendum
# Utils Model
from utils.models import Planta, Area, Cargo
#User
from users.models import User


class CausalSetResource(resources.ModelResource):

    class Meta:
        model = Causal
        fields = ('id', 'nombre', 'centro_costo', 'status', )


class RequerimientoSetResource(resources.ModelResource):
    causal = fields.Field(column_name='causal', attribute='causal', widget=ForeignKeyWidget(Causal, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))
    cliente = fields.Field(column_name='cliente', attribute='cliente', widget=ForeignKeyWidget(Planta, 'nombre'))

    class Meta:
        model = Requerimiento
        fields = ('id', 'codigo', 'centro_costo', 'nombre', 'fecha_solicitud', 'regimen', 'fecha_inicio', 'fecha_termino',
                  'fecha_adendum', 'descripcion', 'bloqueo', 'causal', 'planta', 'cliente', 'status', )


class AreaCargoSetResource(resources.ModelResource):
    requerimiento = fields.Field(column_name='requerimiento', attribute='requerimiento', widget=ForeignKeyWidget(Requerimiento, 'nombre'))
    area = fields.Field(column_name='area', attribute='area', widget=ForeignKeyWidget(Area, 'nombre'))
    cargo = fields.Field(column_name='cargo', attribute='cargo', widget=ForeignKeyWidget(Cargo, 'nombre'))

    class Meta:
        model = AreaCargo
        fields = ('id', 'cantidad', 'valor_aprox', 'fecha_ingreso', 'requerimiento', 'area', 'cargo', 'status', )


class RequerimientoUserSetResource(resources.ModelResource):
    jefe_area = fields.Field(column_name='jefe_area', attribute='jefe_area', widget=ForeignKeyWidget(User, 'nombre'))
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'nombre'))
    area_cargo = fields.Field(column_name='area_cargo', attribute='area_cargo', widget=ForeignKeyWidget(AreaCargo, 'nombre'))

    class Meta:
        mcausalodel = RequerimientoUser
        fields = ('id', 'requerimiento', 'area_cargo', 'user', 'tipo', 'pension', 'jefe_area', 'referido', 'descripcion', 'status', )


class AdendumSetResource(resources.ModelResource):
    requerimiento = fields.Field(column_name='requerimiento', attribute='requerimiento', widget=ForeignKeyWidget(Requerimiento, 'nombre'))

    class Meta:
        model = Adendum
        fields = ('id', 'fecha_inicio', 'fecha_termino', 'requerimiento', 'status', )


@admin.register(Causal)
class CausalAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """CausalAdmin model admin."""

    resource_class = CausalSetResource
    fields = ('nombre', 'descripcion', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', 'descripcion', ]


@admin.register(Requerimiento)
class RequerimientoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """RequerimientoAdmin model admin."""

    resource_class = RequerimientoSetResource
    fields = ('codigo', 'centro_costo', 'nombre', 'fecha_solicitud', 'regimen', 'fecha_inicio', 'fecha_termino',
              'fecha_adendum', 'descripcion', 'bloqueo', 'causal', 'planta','cliente','status', )
    list_display = ('id', 'codigo', 'nombre', 'causal', 'planta', 'status', 'modified',)
    list_filter = ['causal', 'planta','cliente' ,]
    search_fields = ['codigo', 'causal__nombre', 'planta__nombre', 'cliente__nombre',]


@admin.register(AreaCargo)
class AreaCargoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """AreaCargoAdmin model admin."""

    resource_class = AreaCargoSetResource
    fields = ('cantidad', 'valor_aprox', 'fecha_ingreso', 'requerimiento', 'area', 'cargo', 'status', )
    list_display = ('id', 'cantidad', 'requerimiento', 'area', 'cargo', 'status', 'modified',)
    list_filter = ['requerimiento', 'area', 'cargo', ]
    search_fields = ['area__nombre', 'cargo__nombre', 'requerimiento__nombre', ]


@admin.register(RequerimientoUser)
class RequerimientoUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """RequerimientoUserAdmin model admin."""

    resource_class = RequerimientoUserSetResource
    fields = ('requerimiento', 'area_cargo', 'tipo', 'user', 'pension', 'jefe_area', 'referido', 'descripcion', 'status', )
    list_display = ('id', 'user', 'requerimiento', 'area_cargo', 'status', 'modified',)
    list_filter = ['jefe_area', 'user', 'area_cargo' ]
    search_fields = ['tipo', 'jefe_area__nombre', 'user__nombre', 'area_cargo' ]


@admin.register(Adendum)
class AdendumAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """AdendumAdmin model admin."""

    resource_class = AdendumSetResource
    fields = ('fecha_inicio', 'fecha_termino', 'requerimiento', 'status', )
    list_display = ('id', 'fecha_inicio', 'fecha_termino', 'requerimiento', 'status', 'modified',)
    list_filter = ['requerimiento', ]
    search_fields = ['requerimiento__nombre' ]
