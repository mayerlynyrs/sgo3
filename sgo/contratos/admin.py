# Register your models here.
"""Contratos Admin."""

# Django
from django.contrib import admin
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
#Models
from contratos.models import Plantilla, Contrato, DocumentosContrato, TipoDocumento, Finiquito , ContratosBono, ContratosEquipo, Renuncia, Anexo , Revision

class RenunciaSetResource(resources.ModelResource):

    class Meta:
        model = Renuncia
        fields = ('id', 'url','fecha_termino','status', )

class ContratoInLine(admin.TabularInline):

    class Meta:
        model = Contrato
        fields = ('id', 'sueldo_base','fecha_pago', 'fecha_inicio','fecha_termino' ,'fecha_termino_adendum' , 'url' ,'motivo', 'archivado',
        'tipo_contrato','seguro_vida','estado_firma','estado_contrato','fecha_solicitud','fecha_solicitud_baja',
        'fecha_aprobacion','fecha_aprobacion_baja','status', )

class AnexoInLine(admin.TabularInline):

    class Meta:
        model = Anexo
        fields = ('id', 'url','motivo', 'fecha_inicio','fecha_termino_anexo_anterior' ,'fecha_termino' , 'otroanexo','estado_firma',
        'estado_anexo','fecha_solicitud','fecha_solicitud_baja','fecha_aprobacion','fecha_aprobacion_baja','status', )

class TipoDocumentoSetResource(resources.ModelResource):

    class Meta:
        model = TipoDocumento
        fields = ('id', 'nombre','status', )
    
class DocumentoContratoInLine(admin.TabularInline):
    model = DocumentosContrato
    fields = ('archivo', 'status')
    extra = 1

class TipoDocumentoSetResource(resources.ModelResource):

    class Meta:
        model = TipoDocumento
        fields = ('id', 'valor', 'descripcion','status', )

class ContratosBonoSetResource(resources.ModelResource):

    class Meta:
        model = ContratosBono
        fields = ('id', 'nombre','status', )

class FiniquitoSetResource(resources.ModelResource):

    class Meta:
        model = Finiquito
        fields = ('id', 'total_pagar','status', )

class ContratosEquipoSetResource(resources.ModelResource):

    class Meta:
        model = ContratosEquipo
        fields = ('id', 'cantidad','status', )

class RevisionSetResource(resources.ModelResource):

    class Meta:
        model = Revision
        fields = ('id', 'estado','obs','status', )

@admin.register(Plantilla)
class PlantillaAdmin(admin.ModelAdmin):
    """PlantillaAdmin model Admin."""

    fields = ('nombre', 'tipo', 'archivo', 'clientes', 'negocios', 'activo')
    list_display = ('id', 'nombre', 'tipo', 'clientes_list', 'plantas_list', 'activo', 'modified_by', )
    # list_display = ('codigo', 'nombre', 'tipo', 'cliente', 'plantas_list', 'activo', 'modified_by', 'modified', )
    list_filter = ['clientes', 'negocios', ]
    search_fields = ('id', 'nombre', 'tipo', 'clientes_razon_social', 'plantas_nombre', )

    def clientes_list(self, obj):
        return u", ".join(o.razon_social for o in obj.clientes.all())

    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.plantas.all())


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    """ContratoAdmin model Admin."""

    fields = ('sueldo_base','fecha_pago', 'fecha_inicio','fecha_termino' ,'fecha_termino_adendum' , 'url' ,'motivo', 'archivado',
        'tipo_contrato','seguro_vida','estado_firma','estado_contrato','fecha_solicitud','fecha_solicitud_baja',
        'fecha_aprobacion','fecha_aprobacion_baja','usuario','gratificacion','horario','negocio','renuncia','status',)
    list_display = ('id', 'sueldo_base','fecha_pago', 'fecha_inicio','fecha_termino' ,'fecha_termino_adendum' , 'url' ,'motivo', 'archivado',
        'tipo_contrato','seguro_vida','estado_firma','estado_contrato','fecha_solicitud','fecha_solicitud_baja',
        'fecha_aprobacion','fecha_aprobacion_baja',)
    #list_filter = ['usuario__planta', ]
    search_fields = ('usuario__rut', 'usuario__last_name', 'usuario__first_name',)

    

    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.usuario.planta.all())

@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    """AnexoAdmin model Admin."""

    fields = ('url','motivo', 'fecha_inicio','fecha_termino_anexo_anterior' ,'fecha_termino' , 'otroanexo','estado_firma','estado_anexo',
    'fecha_solicitud','fecha_solicitud_baja','fecha_aprobacion','fecha_aprobacion_baja','usuario','contrato','renuncia','negocio','status')
    list_display = ('id', 'motivo', 'fecha_inicio','fecha_termino_anexo_anterior' ,'fecha_termino' , 'otroanexo','estado_firma','estado_anexo',
    'fecha_solicitud','fecha_solicitud_baja','fecha_aprobacion','fecha_aprobacion_baja','status')
    #list_filter = ['usuario__planta', ]
    search_fields = ('usuario__rut', 'usuario__last_name', 'usuario__first_name',)


    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.usuario.planta.all())

@admin.register(DocumentosContrato)
class DocumentoContrato(admin.ModelAdmin):
    """DocumentoContratoAdmnin model Admin."""

    fields = ('contrato', 'tipo_documento','url', 'status' )
    list_display = ('contrato_usuario', 'modified')
    search_fields = ('contrato', )

    def contrato_usuario(self, obj):
        return str(obj.contrato.usuario) + '-' + obj.nombre_archivo


@admin.register(TipoDocumento)
class TipoDocumentoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """TipoDocumentoAdmin model admin."""

    resource_class = TipoDocumentoSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'created',)
    search_fields = ['nombre', ]


@admin.register(Finiquito)
class FiniquitoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """FiniquitoAdmin model admin."""

    resource_class = FiniquitoSetResource
    fields = ('total_pagar','contrato', 'status', )
    list_display = ('id', 'total_pagar', )
    search_fields = ['nombre', ]

@admin.register(ContratosBono)
class ContratosBonoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ContratosBonoAdmin model admin."""

    resource_class = ContratosBonoSetResource
    fields = ('Valor','descripcion', 'contrato', 'bono', 'status', )
    list_display = ('id', 'descripcion' ,'Valor', )
    search_fields = ['nombre', ]

@admin.register(ContratosEquipo)
class ContratosEquipoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ContratosEquipoAdmin model admin."""

    resource_class = ContratosEquipoSetResource
    fields = ('cantidad', 'contrato', 'equipo', 'status', )
    list_display = ('id', 'cantidad' , )
    search_fields = ['nombre', ]

@admin.register(Renuncia)
class RenunciaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """RenunciaAdmin model admin."""

    resource_class = RenunciaSetResource
    fields = ('url','fecha_termino','status' )
    list_display = ('id', 'url', 'fecha_termino',)
    search_fields = ['nombre', ]

@admin.register(Revision)
class RevisionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """RevisionAdmin model admin."""

    resource_class = RevisionSetResource
    fields = ( 'estado','obs','contrato','anexo','status', )
    list_display = ('id', 'estado','obs','contrato','anexo','status',)
    search_fields = ['nombre', ]