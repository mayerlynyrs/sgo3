# Register your models here.
"""Contratos Admin."""

# Django
from django.contrib import admin
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
#Models
from contratos.models import Plantilla, Contrato, DocumentosContrato, Tipo


class TipoSetResource(resources.ModelResource):

    class Meta:
        model = Tipo
        fields = ('id', 'nombre', )


class DocumentoContratoInLine(admin.TabularInline):
    model = DocumentosContrato
    fields = ('archivo',)
    extra = 1

@admin.register(Plantilla)
class PlantillaAdmin(admin.ModelAdmin):
    """PlantillaAdmin model Admin."""

    fields = ('nombre', 'tipo', 'archivo', 'clientes', 'plantas', 'activo')
    list_display = ('id', 'nombre', 'tipo', 'clientes_list', 'plantas_list', 'activo', 'modified_by', )
    # list_display = ('codigo', 'nombre', 'tipo', 'cliente', 'plantas_list', 'activo', 'modified_by', 'modified', )
    list_filter = ['clientes', 'plantas', ]
    search_fields = ('id', 'nombre', 'tipo', 'clientes_razon_social', 'plantas_nombre', )

    def clientes_list(self, obj):
        return u", ".join(o.razon_social for o in obj.clientes.all())

    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.plantas.all())


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    """ContratoAdmin model Admin."""

    fields = ('usuario', 'estado', 'obs', 'archivado')
    list_display = ('usuario', 'plantas_list', 'estado', 'archivado', 'modified', 'created_by')
    #list_filter = ['usuario__planta', ]
    search_fields = ('usuario__rut', 'usuario__last_name', 'usuario__first_name',)

    inlines = [DocumentoContratoInLine]

    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.usuario.planta.all())

@admin.register(DocumentosContrato)
class DocumentoContrato(admin.ModelAdmin):
    """DocumentoContratoAdmnin model Admin."""

    fields = ('contrato', 'archivo', )
    list_display = ('contrato_usuario', 'modified')
    search_fields = ('contrato', )

    def contrato_usuario(self, obj):
        return str(obj.contrato.usuario) + '-' + obj.nombre_archivo


@admin.register(Tipo)
class TipoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """TipoAdmin model admin."""

    resource_class = TipoSetResource
    fields = ('nombre', )
    list_display = ('id', 'nombre', 'created',)
    search_fields = ['nombre', ]
