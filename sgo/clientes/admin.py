from django.contrib import admin

# Register your models here.
"""Clientes Admin."""

# Django
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget
#Models
from clientes.models import Cliente, Negocio, Planta, ContactoPlanta
from utils.models import Region, Provincia, Ciudad, Bono, Gratificacion, Cargo, Area, Horario
from examenes.models import Bateria
from users.models import User


class ClienteSetResource(resources.ModelResource):

    horario = fields.Field(column_name='horario', attribute='horario',widget=ManyToManyWidget(Horario, ',', 'pk'))
    area = fields.Field(column_name='area', attribute='area',widget=ManyToManyWidget(Area, ',', 'pk'))
    cargo = fields.Field(column_name='cargo', attribute='cargo',widget=ManyToManyWidget(Cargo, ',', 'pk'))
    ciudad = fields.Field(column_name='ciudad', attribute='ciudad', widget=ForeignKeyWidget(Ciudad, 'nombre'))

    class Meta:
        model = Cliente
        fields = ('id', 'rut', 'razon_social', 'abreviatura', 'email', 'telefono', 'ciudad', 'direccion_comercial', )


class NegocioSetResource(resources.ModelResource):

    cliente = fields.Field(column_name='cliente', attribute='cliente',widget=ManyToManyWidget(Cliente, ',', 'razon_social'))

    class Meta:
        model = Negocio
        fields = ('id', 'nombre', 'descripcion', 'archivo', 'status',)


class PlantaSetResource(resources.ModelResource):

    ciudad = fields.Field(column_name='ciudad', attribute='ciudad', widget=ForeignKeyWidget(Ciudad, 'nombre'))
    negocio = fields.Field(column_name='negocio', attribute='negocio', widget=ForeignKeyWidget(Negocio, 'nombre'))
    gratificacion = fields.Field(column_name='gratificacion', attribute='gratificacion', widget=ForeignKeyWidget(Gratificacion, 'nombre'))
    bateria = fields.Field(column_name='bateria', attribute='bateria', widget=ManyToManyWidget(Bateria, 'nombre'))
    bono = fields.Field(column_name='bono', attribute='bono',widget=ManyToManyWidget(Bono, ',', 'pk'))

    class Meta:
        model = Planta
        fields = ('id', 'rut', 'nombre', 'cliente', 'rut_representante', 'representante_legal', 'region', 'provincia', 'ciudad', 'direccion_comercial', 'bateria', 'psicologico', 'hal2')


class ContactoPlantaSetResource(resources.ModelResource):

    cliente = fields.Field(column_name='cliente', attribute='cliente',widget=ForeignKeyWidget(Cliente, 'razon_social'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'nombre'))

    class Meta:
        model = ContactoPlanta
        fields = ('id', 'rut', 'nombres', 'apellidos', 'fecha_nacimiento', 'telefono', 'email', 'relacion', 'cliente', 'planta', 'user',)


@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ClienteAdmin model Admin"""

    # resource_class = ClienteSetResource
    fields = ('rut', 'razon_social', 'giro', 'abreviatura', 'email', 'telefono', 'area','cargo', 'horario' , 'region', 'provincia', 'ciudad', 'direccion', 'status', )
    list_display = ('id', 'razon_social', 'ciudad', 'area_list', 'cargo_list', )
    list_filter = ['area', 'cargo', ]
    search_fields = ('id', 'razon_social', 'area__nombre', 'cargo__nombre')

    def area_list(self, obj):
        return u", ".join(o.nombre for o in obj.area.all())

    def cargo_list(self, obj):
        return u", ".join(o.nombre for o in obj.cargo.all())



# @admin.register(Cliente)
# class ClienteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     """ClienteAdmin model admin."""

#     resource_class = ClienteSetResource
#     fields = ('rut', 'razon_social', 'giro', 'email', 'telefono', 'area','cargo', 'horario' , 'region', 'provincia', 'ciudad', 'direccion', 'status', )
#     list_display = ('id', 'rut', 'razon_social', 'ciudad',)
#     search_fields = ['razon_social', ]


@admin.register(Negocio)
class NegocioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """NegocioAdmin model admin."""

    resource_class = NegocioSetResource
    fields = ('cliente', 'nombre', 'descripcion', 'archivo', 'status', )
    list_display = ('id', 'nombre', 'cliente')
    search_fields = ('nombre', )


@admin.register(Planta)
class PlantaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """PlantaAdmin model admin."""

    resource_class = PlantaSetResource
    fields = ('cliente', 'negocio', 'rut', 'nombre', 'rut_gerente', 'nombre_gerente', 'direccion_gerente', 'telefono', 'email', 'gratificacion', 'region', 'provincia', 'ciudad', 'direccion', 'bono', 'bateria', 'psicologico', 'hal2', 'status',)
    list_display = ('id', 'nombre', 'cliente', 'negocio', 'nombre_gerente', 'ciudad',)
    search_fields = ['nombre', ]


@admin.register(ContactoPlanta)
class ContactoPlantaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ContactoPlantaAdmin model admin."""

    resource_class = ContactoPlantaSetResource
    fields = ('rut', 'nombres', 'apellidos', 'fecha_nacimiento', 'telefono', 'email', 'relacion', 'cliente', 'planta', 'user', 'status',)
    list_display = ('id', 'nombres', 'apellidos', 'relacion', 'planta', 'user',)
    search_fields = ['nombres', ]
