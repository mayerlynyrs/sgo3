from django.contrib import admin

# Register your models here.
"""Utils Admin."""

# Django
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget
#Models
from utils.models import Region, Provincia, Ciudad, Bono, Gratificacion, Cliente, Negocio, Planta, Cargo, Area,  PuestaDisposicion , Abastecimiento, Horario, Equipo


class RegionSetResource(resources.ModelResource):

    class Meta:
        model = Region
        fields = ('id', 'nombre', 'status', )


class ProvinciaSetResource(resources.ModelResource):
    region = fields.Field(column_name='region', attribute='region', widget=ForeignKeyWidget(Region, 'nombre'))

    class Meta:
        model = Provincia
        fields = ('id', 'nombre', 'region', 'status', )


class CiudadSetResource(resources.ModelResource):
    provincia = fields.Field(column_name='provincia', attribute='provincia', widget=ForeignKeyWidget(Provincia, 'nombre'))

    class Meta:
        model = Ciudad
        fields = ('id', 'nombre', 'provincia', 'status', )

class BonoSetResource(resources.ModelResource):

    class Meta:
        model = Bono
        fields = ('id', 'nombre', 'descripcion', 'status', )


class GratificacionSetResource(resources.ModelResource):

    class Meta:
        model = Gratificacion
        fields = ('id', 'nombre', 'descripcion', 'status', )

class CargoSetResource(resources.ModelResource):

    class Meta:
        model = Cargo
        fields = ('id', 'nombre','descripcion' ,'status', )


class AreaSetResource(resources.ModelResource):

    class Meta:
        model = Area
        fields = ('id', 'nombre', 'status', )

class HorarioSetResource(resources.ModelResource):

    class Meta:
        model = Horario
        fields = ('id', 'nombre', 'descripcion', 'status',  )

class ClienteSetResource(resources.ModelResource):

    horario = fields.Field(column_name='horario', attribute='horario',widget=ManyToManyWidget(Horario, ',', 'pk'))
    area = fields.Field(column_name='area', attribute='area',widget=ManyToManyWidget(Area, ',', 'pk'))
    cargo = fields.Field(column_name='cargo', attribute='cargo',widget=ManyToManyWidget(Cargo, ',', 'pk'))
    ciudad = fields.Field(column_name='ciudad', attribute='ciudad', widget=ForeignKeyWidget(Ciudad, 'nombre'))

    class Meta:
        model = Cliente
        fields = ('id', 'rut', 'razon_social', 'ciudad', 'direccion_comercial', )


class NegocioSetResource(resources.ModelResource):

    cliente = fields.Field(column_name='cliente', attribute='cliente',widget=ManyToManyWidget(Cliente, ',', 'razon_social'))

    class Meta:
        model = Negocio
        fields = ('id', 'nombre', 'descripcion', 'archivo', 'status',)
 


class PlantaSetResource(resources.ModelResource):

    ciudad = fields.Field(column_name='ciudad', attribute='ciudad', widget=ForeignKeyWidget(Ciudad, 'nombre'))
    negocio = fields.Field(column_name='negocio', attribute='negocio', widget=ForeignKeyWidget(Negocio, 'razon_social'))
    gratificacion = fields.Field(column_name='gratificacion', attribute='gratificacion', widget=ForeignKeyWidget(Gratificacion, 'razon_social'))
    bono = fields.Field(column_name='bono', attribute='bono',widget=ManyToManyWidget(Bono, ',', 'pk'))

    class Meta:
        model = Planta
        fields = ('id', 'nombre', 'cliente', 'ciudad', 'direccion_comercial', 'provincia', 'region', 'rut_representante', 'representante_legal', )

class PuestaDisposicionSetResource(resources.ModelResource):

    class Meta:
        model = PuestaDisposicion
        fields = ('id', 'nombre', 'gratificacion', 'seguro_cesantia', 'seguro_invalidez', 'seguro_vida', 'mutual', 'status', )

class AbastecimientoSetResource(resources.ModelResource):
    negocio = fields.Field(column_name='negocio', attribute='negocio', widget=ForeignKeyWidget(Negocio, 'razon_social'))

    class Meta:
        model = Abastecimiento
        fields = ('id', 'tipo', 'insumos', 'status',  )

class EquipoSetResource(resources.ModelResource):
    cliente = fields.Field(column_name='cliente', attribute='cliente', widget=ForeignKeyWidget(Cliente, 'razon_social'))

    class Meta:
        model = Equipo
        fields = ('id', 'nombre', 'cliente', 'valor',  'tipo' 'status',  )

@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """RegionAdmin model admin."""

    resource_class = RegionSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre',)
    search_fields = ['nombre', ]


@admin.register(Provincia)
class ProvinciaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ProvinciaAdmin model admin."""

    resource_class = ProvinciaSetResource
    fields = ('region', 'nombre', 'status', )
    list_display = ('id', 'nombre', 'region',)
    list_filter = ['region', ]
    search_fields = ('nombre', 'region__nombre')


@admin.register(Ciudad)
class CiudadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """CiudadAdmin model admin."""

    resource_class = CiudadSetResource
    fields = ('provincia', 'nombre', 'status', )
    list_display = ('id', 'nombre', 'provincia',)
    list_filter = ['provincia', ]
    search_fields = ('nombre', 'provincia__nombre')

@admin.register(Bono)
class BonoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """BonoAdmin model admin."""

    resource_class = BonoSetResource
    fields = ('nombre', 'descripcion', 'status', )
    list_display = ('id', 'nombre', 'descripcion',)
    search_fields = ['nombre', ]


@admin.register(Gratificacion)
class GratificacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """GratificacionAdmin model admin."""

    resource_class = GratificacionSetResource
    fields = ('nombre', 'descripcion', 'status',)
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]

@admin.register(Cargo)
class CargoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """CargoAdmin model admin."""

    resource_class = CargoSetResource
    fields = ('nombre', 'descripcion','status', )
    list_display = ('id', 'nombre', 'descripcion',)
    search_fields = ['nombre', ]


@admin.register(Area)
class AreaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """AreaAdmin model admin."""

    resource_class = AreaSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre',)
    search_fields = ['nombre', ]

@admin.register(Horario)
class HorarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """HorarioAdmin model admin."""

    resource_class = HorarioSetResource
    fields = ( 'nombre', 'descripcion', 'status', )
    list_display = ('id', 'nombre', 'descripcion', )
    search_fields = ['nombre', ]

@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ClienteAdmin model admin."""

    resource_class = ClienteSetResource
    fields = ('rut', 'razon_social', 'giro', 'email', 'telefono', 'area','cargo', 'horario' , 'region', 'provincia', 'ciudad', 'direccion', 'status', )
    list_display = ('id', 'rut', 'razon_social', 'ciudad',)
    search_fields = ['razon_social', ]


@admin.register(Negocio)
class NegocioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """NegocioAdmin model admin."""

    resource_class = NegocioSetResource
    fields = ('cliente', 'nombre', 'descripcion', 'archivo', 'status', )
    list_display = ('id', 'nombre', )
    search_fields = ('nombre', )

@admin.register(Planta)
class PlantaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """PlantaAdmin model admin."""

    resource_class = PlantaSetResource
    fields = ('nombre', 'rut_gerente', 'nombre_gerente', 'direccion_gerente', 'telefono', 'email', 'gratificacion', 'negocio', 'region', 'provincia', 'ciudad', 'direccion', 'bono', 'status', )
    list_display = ('id', 'nombre', 'rut_gerente', 'nombre_gerente', 'ciudad',)
    search_fields = ['nombre', ]

@admin.register(PuestaDisposicion)
class PuestaDisposicionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """PuestaDisposicionAdmin model admin."""

    resource_class = PuestaDisposicionSetResource
    fields = ('nombre' , 'gratificacion', 'seguro_cesantia', 'seguro_invalidez', 'seguro_vida', 'mutual', 'status', )
    list_display = ('id', 'nombre', 'gratificacion', 'seguro_cesantia', 'seguro_invalidez', 'seguro_vida', 'mutual',)
    search_fields = ['nombre', ]

@admin.register(Abastecimiento)
class AbastecimientoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """AbastecimientoAdmin model admin."""

    resource_class = AbastecimientoSetResource
    fields = ( 'tipo', 'insumos','negocio', 'status',  )
    list_display = ('id', 'tipo', 'insumos',  )
    search_fields = ['tipo', 'insumos']


@admin.register(Equipo)
class EquipoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """EquipoAdmin model admin."""

    resource_class = EquipoSetResource
    fields = ( 'nombre', 'valor',  'tipo' ,'cliente', 'status', )
    list_display = ('id','nombre', 'valor',  'tipo' , 'cliente' )
    list_filter = ['cliente', ]
    search_fields = ['nombre', 'tipo', ]
# admin.site.register(Region)
