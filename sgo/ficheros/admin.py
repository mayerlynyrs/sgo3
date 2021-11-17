"""Utils Admin."""

# Django
from django.contrib import admin
# django-import-export
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from import_export.admin import ImportExportModelAdmin
#Models
from ficheros.models import Fichero, Publicacion
# Utils Model
from utils.models import Cliente, Negocio
#User
from users.models import Especialidad


class FicheroSetResource(resources.ModelResource):
    clientes = fields.Field(
        column_name='clientes',
        attribute='clientes',
        widget=ManyToManyWidget(Cliente, ',', 'pk'))

    negocios = fields.Field(
        column_name='negocios',
        attribute='negocios',
        widget=ManyToManyWidget(Negocio, ',', 'pk'))


    class Meta:
        model = Fichero
        fields = ('id', 'nombre', 'desc', 'clientes', 'negocios')


class PublicacionSetResource(resources.ModelResource):
    especialidades = fields.Field(
        column_name='especialidades',
        attribute='especialidades',
        widget=ManyToManyWidget(Publicacion, ',', 'pk'))


    class Meta:
        model = Publicacion
        fields = ('id', 'nombre', 'descripcion', 'especialidades')


@admin.register(Fichero)
class FicheroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """FicheroAdmin model Admin"""

    # resource_class = FicheroSetResource
    fields = ('nombre', 'desc', 'url', 'clientes', 'negocios', 'status', )
    list_display = ('id', 'nombre', 'clientes_list', 'negocios_list', 'modified_by')
    list_filter = ['clientes', 'negocios', ]
    search_fields = ('id', 'nombre', 'clientes__razon_social', 'negocios__nombre')

    def clientes_list(self, obj):
        return u", ".join(o.razon_social for o in obj.clientes.all())

    def negocios_list(self, obj):
        return u", ".join(o.nombre for o in obj.negocios.all())


@admin.register(Publicacion)
class PublicacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """PublicacionAdmin model Admin"""

    fields = ('nombre', 'descripcion', 'especialidades', 'status', )
    list_display = ('id', 'nombre', 'especialidades_list', 'modified_by')
    list_filter = ['especialidades', ]
    search_fields = ('id', 'nombre', 'especialidades__nombre')

    def especialidades_list(self, obj):
        return u", ".join(o.nombre for o in obj.especialidades.all())
