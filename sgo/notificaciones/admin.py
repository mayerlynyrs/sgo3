from django.contrib import admin
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from notificaciones.models import Tipo, Destinatario

class TipoSetResource(resources.ModelResource):

    class Meta:
        model = Tipo
        fields = ('id', 'nombre', 'sub_tipo', 'status', )

class DestinatarioSetResource(resources.ModelResource):
    tipo = fields.Field(column_name='tipo', attribute='tipo', widget=ForeignKeyWidget(Tipo, 'nombre'))
    class Meta:
        model = Destinatario
        fields = ('id', 'notifica_sistema', 'fecha_notificacion', 'fecha_apertura', 'status', )


@admin.register(Tipo)
class TipoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """TipoAdmin model admin."""

    resource_class = TipoSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'created',)
    search_fields = ['nombre', ]

@admin.register(Destinatario)
class DestinatarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """DestinatarioAdmin model admin."""

    resource_class = DestinatarioSetResource
    fields = ('tipo', 'notifica_sistema', 'fecha_notificacion', 'fecha_apertura', 'status',  )
    list_display = ('id', 'notifica_sistema', 'fecha_notificacion', 'fecha_apertura',)
    search_fields = ['nombre', ]
