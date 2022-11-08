# Register your models here.
"""Contratos Admin."""

# Django
from django.contrib import admin
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
#Models
from contratos.models import Plantilla, TipoContrato, Contrato, DocumentosContrato, TipoDocumento, Finiquito, ContratosBono, ContratosEquipo, FinRequerimiento, Anexo, Revision, MotivoBaja
from requerimientos.models import RequerimientoTrabajador, Causal
# Clientes
from clientes.models import Planta
from utils.models import Gratificacion, Horario, Bono, Equipo
from users.models import User, ValoresDiario

class FinRequerimientoSetResource(resources.ModelResource):
    requerimiento_trabajador = fields.Field(column_name='requerimiento_trabajador', attribute='requerimiento_trabajador', widget=ForeignKeyWidget(RequerimientoTrabajador, 'nombre'))
    class Meta:
        model = FinRequerimiento
        fields = ('id', 'tipo', 'archivo', 'fecha_termino', 'motivo', 'status',)

class TipoContratoSetResource(resources.ModelResource):

    class Meta:
        model = TipoContrato
        fields = ('id', 'nombre','status', )

class ContratoInLine(admin.TabularInline):

    requerimiento_trabajador = fields.Field(column_name='requerimiento_trabajador', attribute='requerimiento_trabajador', widget=ForeignKeyWidget(RequerimientoTrabajador, 'nombre'))
    tipo_documento = fields.Field(column_name='tipo_documento', attribute='tipo_documento', widget=ForeignKeyWidget(TipoDocumento, 'nombre'))
    gratificacion = fields.Field(column_name='gratificacion', attribute='gratificacion', widget=ForeignKeyWidget(Gratificacion, 'nombre'))
    horario = fields.Field(column_name='horario', attribute='horario', widget=ForeignKeyWidget(Horario, 'nombre'))
    fin_requerimiento = fields.Field(column_name='fin_requerimiento', attribute='fin_requerimiento', widget=ForeignKeyWidget(FinRequerimiento, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'nombre'))
    causal = fields.Field(column_name='causal', attribute='causal', widget=ForeignKeyWidget(Causal, 'nombre'))
    valores_diario = fields.Field(column_name='valores_diario', attribute='valores_diario', widget=ForeignKeyWidget(ValoresDiario, 'valor_diario'))
    
    class Meta:
        model = Contrato
        fields = ('id', 'sueldo_base','fecha_pago', 'fecha_inicio','fecha_termino' ,'fecha_termino_ultimo_anexo' , 'archivo' ,'motivo', 'archivado',
        'seguro_vida','estado_firma','estado_contrato','fecha_solicitud','fecha_solicitud_baja',
        'fecha_aprobacion','fecha_aprobacion_baja', 'status', )

class AnexoInLine(admin.TabularInline):

    requerimiento_trabajador = fields.Field(column_name='requerimiento_trabajador', attribute='requerimiento_trabajador', widget=ForeignKeyWidget(RequerimientoTrabajador, 'nombre'))
    horario = fields.Field(column_name='horario', attribute='horario', widget=ForeignKeyWidget(Horario, 'nombre'))
    fin_requerimiento = fields.Field(column_name='fin_requerimiento', attribute='fin_requerimiento', widget=ForeignKeyWidget(FinRequerimiento, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'nombre'))
    causal = fields.Field(column_name='causal', attribute='causal', widget=ForeignKeyWidget(Causal, 'nombre'))

    class Meta:
        model = Anexo
        fields = ('id', 'archivo','motivo', 'fecha_inicio','fecha_termino_anexo_anterior' ,'fecha_termino' , 'estado_firma',
        'estado_anexo','fecha_solicitud','fecha_solicitud_baja','fecha_aprobacion','fecha_aprobacion_baja','status', )

class TipoDocumentoSetResource(resources.ModelResource):

    class Meta:
        model = TipoDocumento
        fields = ('id', 'nombre', 'status', )
    
class DocumentoContratoInLine(admin.TabularInline):
    contrato = fields.Field(column_name='contrato', attribute='contrato', widget=ForeignKeyWidget(Contrato, 'nombre'))
    tipo_documento = fields.Field(column_name='tipo_documento', attribute='tipo_documento', widget=ForeignKeyWidget(TipoDocumento, 'nombre'))

    model = DocumentosContrato
    fields = ('archivo', 'status')
    extra = 1

class ContratosBonoSetResource(resources.ModelResource):
    contrato = fields.Field(column_name='contrato', attribute='contrato', widget=ForeignKeyWidget(Contrato, 'nombre'))
    bono = fields.Field(column_name='bono', attribute='bono', widget=ForeignKeyWidget(Bono, 'nombre'))
    
    class Meta:
        model = ContratosBono
        fields = ('id', 'valor','status', )

class FiniquitoSetResource(resources.ModelResource):
    contrato = fields.Field(column_name='contrato', attribute='contrato', widget=ForeignKeyWidget(Contrato, 'nombre'))

    class Meta:
        model = Finiquito
        fields = ('id', 'total_pagar','status', )

class ContratosEquipoSetResource(resources.ModelResource):
    contrato = fields.Field(column_name='contrato', attribute='contrato', widget=ForeignKeyWidget(Contrato, 'nombre'))
    equipo = fields.Field(column_name='equipo', attribute='equipo', widget=ForeignKeyWidget(Equipo, 'nombre'))

    class Meta:
        model = ContratosEquipo
        fields = ('id', 'cantidad','status', )

class RevisionSetResource(resources.ModelResource):
    contrato = fields.Field(column_name='contrato', attribute='contrato', widget=ForeignKeyWidget(Contrato, 'nombre'))
    anexo = fields.Field(column_name='anexo', attribute='anexo', widget=ForeignKeyWidget(Anexo, 'nombre'))
    class Meta:
        model = Revision
        fields = ('id', 'estado','obs','status', )

class MotivoBajaSetResource(resources.ModelResource):

    class Meta:
        model = MotivoBaja
        fields = ('id', 'nombre', 'status', )

@admin.register(Plantilla)
class PlantillaAdmin(admin.ModelAdmin):
    """PlantillaAdmin model Admin."""

    fields = ('nombre', 'tipo', 'abreviatura', 'archivo', 'clientes', 'plantas', 'activo')
    list_display = ('id', 'nombre', 'tipo', 'abreviatura', 'clientes_list', 'plantas_list', 'activo', 'modified_by', )
    # list_display = ('codigo', 'nombre', 'tipo', 'cliente', 'plantas_list', 'activo', 'modified_by', 'modified', )
    list_filter = ['clientes', 'plantas', ]
    search_fields = ('id', 'nombre', 'tipo', 'abreviatura', 'clientes_razon_social', 'plantas_nombre', )

    def clientes_list(self, obj):
        return u", ".join(o.razon_social for o in obj.clientes.all())

    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.plantas.all())


@admin.register(TipoContrato)
class TipoContratoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """TipoContratoAdmin model admin."""

    resource_class = TipoContratoSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'created',)
    search_fields = ['nombre', ]


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    """ContratoAdmin model Admin."""

    fields = ('sueldo_base','fecha_pago', 'fecha_inicio','fecha_termino' ,'fecha_termino_ultimo_anexo' , 'archivo' ,'motivo', 'archivado',
        'tipo_documento','seguro_vida','estado_firma','estado_contrato','fecha_solicitud','fecha_solicitud_baja',
        'fecha_aprobacion','fecha_aprobacion_baja','trabajador','gratificacion','horario','planta','causal','fin_requerimiento','requerimiento_trabajador','valores_diario','obs','status',)
    list_display = ('id', 'sueldo_base','fecha_pago', 'fecha_inicio','fecha_termino' ,'fecha_termino_ultimo_anexo' , 'archivo' ,'motivo', 'archivado',
        'tipo_documento','seguro_vida','estado_firma','estado_contrato','fecha_solicitud','fecha_solicitud_baja',
        'fecha_aprobacion','fecha_aprobacion_baja',)
    # list_filter = ['user__planta', ]
    search_fields = ('trabajador__rut', 'trabajador__last_name', 'trabajador__first_name',)

    

    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.usuario.planta.all())

@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    """AnexoAdmin model Admin."""

    fields = ('archivo','motivo', 'fecha_inicio','fecha_termino_anexo_anterior' ,'fecha_termino' ,'estado_firma','estado_anexo',
    'fecha_solicitud','fecha_solicitud_baja','fecha_aprobacion','fecha_aprobacion_baja','trabajador','contrato','fin_requerimiento','requerimiento_trabajador','planta','status')
    list_display = ('id', 'motivo', 'fecha_inicio','fecha_termino_anexo_anterior' ,'fecha_termino' ,'estado_firma','estado_anexo',
    'fecha_solicitud','fecha_solicitud_baja','fecha_aprobacion','fecha_aprobacion_baja','status')
    # list_filter = ['user__planta', ]
    search_fields = ('trabajador__rut', 'trabajador__last_name', 'trabajador__first_name',)


    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.usuario.planta.all())

@admin.register(DocumentosContrato)
class DocumentoContrato(admin.ModelAdmin):
    """DocumentoContratoAdmnin model Admin."""

    fields = ('contrato', 'tipo_documento','archivo', 'status' )
    list_display = ('contrato_trabajador', 'modified')
    search_fields = ('contrato', )

    def contrato_trabajador(self, obj):
        return str(obj.contrato.trabajador) + '-' + obj.nombre_archivo


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
    fields = ('valor', 'contrato', 'bono', 'status', )
    list_display = ('id', 'contrato', 'bono', 'valor', )
    search_fields = ['valor', ]

@admin.register(ContratosEquipo)
class ContratosEquipoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ContratosEquipoAdmin model admin."""

    resource_class = ContratosEquipoSetResource
    fields = ('cantidad', 'contrato', 'equipo', 'status', )
    list_display = ('id', 'cantidad' , )
    search_fields = ['nombre', ]

@admin.register(FinRequerimiento)
class FinRequerimientoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """FinRequerimientoAdmin model admin."""

    resource_class = FinRequerimientoSetResource
    fields = ('tipo', 'archivo','fecha_termino', 'requerimiento_trabajador', 'motivo', 'status')
    list_display = ('id', 'tipo', 'archivo', 'fecha_termino', 'motivo')
    search_fields = ['tipo', ]

@admin.register(Revision)
class RevisionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """RevisionAdmin model admin."""

    resource_class = RevisionSetResource
    fields = ( 'estado','obs','contrato','anexo','status', )
    list_display = ('id', 'estado','obs','contrato','anexo','status',)
    search_fields = ['nombre', ]

@admin.register(MotivoBaja)
class MotivoBajaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """MotivoBajaAdmin model admin."""

    resource_class = MotivoBajaSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre',)
    search_fields = ['nombre', ]