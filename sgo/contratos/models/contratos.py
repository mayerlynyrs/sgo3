"""Contratos model."""
from asyncio.windows_events import NULL
import os
import re

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.forms import model_to_dict
from django.core.validators import FileExtensionValidator
# Models
from users.models import Trabajador, ValoresDiario
# Clientes
from clientes.models import Planta, Cliente
# Utilities
from utils.models import BaseModel, Bono, Equipo, Gratificacion, Horario
from contratos.models import TipoDocumento
from requerimientos.models import RequerimientoTrabajador, Causal, Requerimiento

User = get_user_model()


class Renuncia(BaseModel):
    nombre = models.CharField(max_length=250)
    archivo = models.FileField(
        upload_to='renuncias/',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', ])]
    )
    fecha_termino = models.DateField(blank=True, null=True)
    requerimiento_trabajador = models.ForeignKey(RequerimientoTrabajador, on_delete=models.PROTECT)
    
    
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el bono, deshabilite esta casilla.'
    )
    
    def __str__(self):
        return self.nombre


class TipoContrato(BaseModel):
    nombre = models.CharField(
                max_length = 60,
                unique = True
                )
    status = models.BooleanField(
                default=True,
                help_text='para desactivar el tipo de contrato, deshabilite esta casilla.'
                )

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        return item


class Contrato(BaseModel):
    POR_FIRMAR = 'PF'
    ENVIADO_FIRMAR = 'EF'
    FIRMADO_TRABAJADOR = 'FT'
    FIRMADO_EMPLEADOR = 'FE'
    FIRMADO = 'FF'
    OBJETADO = 'OB'

    CREADO = 'CR'
    RECHAZADO ='RC'
    PROCESO_VALIDACION = 'PV'
    APROBADO = 'AP'
    PENDIENTE_BAJA ='PB'
    BAJADO = 'BJ'

    NORMAL = 'NOR'
    PARADA_GENERAL_PLANTA = 'PGP'
    URGENCIA = 'URG'

    REGIMEN_ESTADO = (
        (NORMAL, 'Normal'),
        (PARADA_GENERAL_PLANTA, 'Parada Planta'),
        (URGENCIA, 'Urgencia'),
    )


    FIRMA_ESTADO = (
        (POR_FIRMAR, 'Por Firmar'),
        (ENVIADO_FIRMAR, 'Enviado a Firmar'),
        (FIRMADO_TRABAJADOR, 'Firmado por Trabajador'),
        (FIRMADO_EMPLEADOR, 'Firmado por Empleador'),
        (FIRMADO, 'Firmado'),
        (OBJETADO, 'Objetado'),
    )

    CONTRATO_ESTADO = (
        (CREADO, 'Creado'),
        (RECHAZADO, 'Rechazado'),
        (PROCESO_VALIDACION, 'En Proceso de Validación'),
        (APROBADO, 'Aprobado'),
        (PENDIENTE_BAJA,'En Proceso de Baja'),
        (BAJADO,'Bajado'),
    )

    sueldo_base = models.IntegerField(default=0)
    fecha_pago = models.DateField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=False, null=False)
    fecha_termino = models.DateField(blank=False, null=False)
    fecha_termino_ultimo_anexo = models.DateField(blank=True, null=True)
    archivo = models.FileField(
        upload_to='contratos/',
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])]
    )
    motivo = models.TextField(blank=True, null=True)
    archivado = models.BooleanField(default=False)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)
    seguro_vida = models.BooleanField(
        default=False,
        help_text='Para desactivar el seguro de vida, deshabilite esta casilla.'
    )
    estado_firma = models.CharField(max_length=2, choices=FIRMA_ESTADO, default=POR_FIRMAR)
    estado_contrato = models.CharField(max_length=2, choices=CONTRATO_ESTADO, default=CREADO)
    fecha_solicitud = models.DateTimeField(blank=True, null=True)
    fecha_solicitud_baja = models.DateTimeField(blank=True, null=True)
    fecha_aprobacion = models.DateTimeField(blank=True, null=True)
    fecha_aprobacion_baja = models.DateTimeField(blank=True, null=True)
    nueva_renta = models.IntegerField(default=0)
    obs = models.TextField(blank=True, null=True)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT)
    gratificacion = models.ForeignKey(Gratificacion, on_delete=models.PROTECT)
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT)
    renuncia = models.ForeignKey(Renuncia, on_delete=models.PROTECT, blank=True, null=True)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT)
    requerimiento_trabajador = models.ForeignKey(RequerimientoTrabajador, on_delete=models.PROTECT)
    causal = models.ForeignKey(Causal, on_delete=models.PROTECT)
    regimen = models.CharField(max_length=3, choices=REGIMEN_ESTADO, default=NORMAL)
    valores_diario = models.ForeignKey(ValoresDiario, on_delete=models.PROTECT, blank=True, null=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el contrato , deshabilite esta casilla.'
    )
    def __str__(self):
        return str(self.trabajador.rut) + '-' + str(self.id).zfill(4)
    
    def toJSON(self):
        item = model_to_dict(self) 
        item['archivo'] = str(self.archivo).zfill(0)
        if(self.valores_diario):
            item['contrato'] = "Tipo: " + self.tipo_documento.nombre.title() + " <br> Causal: " + self.causal.nombre.title() + "<br> Motivo:  " + self.motivo + "<br> Jornada:  " + self.horario.nombre.title() + "<br> Renta:  " + str(self.valores_diario.valor_diario)
        else:
            item['contrato'] = "Tipo: " + self.tipo_documento.nombre.title() +  "<br> Causal: " + self.causal.nombre.title() + "<br> Motivo:  " + self.motivo + "<br> Jornada:  " + self.horario.nombre.title() + "<br> Renta:  " + str(self.sueldo_base)  
        item['requerimiento'] = self.requerimiento_trabajador.requerimiento.nombre.title() + "<br> Planta : " + self.planta.nombre.title()
        # item['requerimiento'] = self.requerimiento_trabajador.requerimiento.nombre.title() + "<br> Planta : " + self.planta.nombre.title() + "<br> Solicitante: " + self.created_by.first_name.title() + " " + self.created_by.last_name.title()
        item['trabajador'] = self.trabajador.first_name.title() + " " + self.trabajador.last_name.title() + "<br>" + self.trabajador.rut + "<br>" + self.trabajador.email
        item['nombre'] = self.trabajador.first_name.title() + " " + self.trabajador.last_name.title()
        item['plazos'] = "Fecha Inicio: "+ str(self.fecha_inicio.strftime('%d-%m-%Y')) + "<br> Fecha Término:  " + str(self.fecha_termino.strftime('%d-%m-%Y'))    
        item['solicitante'] = self.created_by.first_name.title() + " " + self.created_by.last_name.title()
        item['estado_firma'] = self.estado_firma
        return item


def contrato_directory_path(instance, filename):
    return '/'.join(['contratos', str(instance.contrato.trabajador.id), filename])


#DocAdicional
class DocumentosContrato(BaseModel):
    archivo = models.FileField(upload_to=contrato_directory_path,
                               validators=[
                                   FileExtensionValidator(allowed_extensions=['pdf', ])])
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el Documento, deshabilite esta casilla.'
    )

    class Meta:
        ordering = ['contrato']
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return str(self.contrato.trabajador) + '-' + self.nombre_archivo
    
    def toJSON(self):
        item = model_to_dict(self) 
        item['archivo'] = str(self.archivo).zfill(0)
        item['contrato'] = self.contrato.id
        item['tipo_documento_id'] = self.tipo_documento.id
        item['tipo_documento'] = self.tipo_documento.nombre.title()
        return item

    @property
    def nombre_archivo(self):
        return os.path.basename(self.archivo.name)


class ContratosBono(models.Model):
    valor = models.IntegerField(default=0)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    bono = models.ForeignKey(Bono, on_delete=models.CASCADE)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el bono, deshabilite esta casilla.'
    )                                                                                                                                                                                                                
    created_date = models.DateTimeField(
        default= timezone.now,
        null=True,
        blank=True
    )
    def __str__(self):
        return str(self.valor)


class Anexo(BaseModel):
    POR_FIRMAR = 'PF'
    ENVIADO_FIRMAR = 'EF'
    FIRMADO_TRABAJADOR = 'FT'
    FIRMADO_EMPLEADOR = 'FE'
    FIRMADO = 'FF'
    OBJETADO = 'OB'

    CREADO = 'CR'
    PROCESO_VALIDACION = 'PV'
    APROBADO = 'AP'
    PENDIENTE_BAJA ='PB'
    BAJADO = 'BJ'

    FIRMA_ESTADO = (
        (POR_FIRMAR, 'Por Firmar'),
        (ENVIADO_FIRMAR, 'Enviado a Firmar'),
        (FIRMADO_TRABAJADOR, 'Firmado por Trabajador'),
        (FIRMADO_EMPLEADOR, 'Firmado por Empleador'),
        (FIRMADO, 'Firmado'),
        (OBJETADO, 'Objetado'),
    )

    ANEXO_ESTADO = (
        (CREADO, 'Creado'),
        (PROCESO_VALIDACION, 'en Proceso de  Validacion'),
        (APROBADO, 'Aprobado'),
        (PENDIENTE_BAJA,'en Proceso de baja'),
        (BAJADO,'Bajado'),
    )

    
    archivo = models.FileField(
        upload_to='anexos/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])]
    )
    motivo = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=False, null=False)
    fecha_termino_anexo_anterior = models.DateField(blank=False, null=False)
    fecha_termino = models.DateField(blank=False, null=False)
    estado_firma = models.CharField(max_length=2, choices=FIRMA_ESTADO, default=POR_FIRMAR)
    estado_anexo = models.CharField(max_length=2, choices=ANEXO_ESTADO, default=CREADO)
    fecha_solicitud = models.DateTimeField(blank=True, null=True)
    fecha_solicitud_baja = models.DateTimeField(blank=True, null=True)
    fecha_aprobacion = models.DateTimeField(blank=True, null=True)
    fecha_aprobacion_baja = models.DateTimeField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el anexo, deshabilite esta casilla.'
    )

    nueva_renta = models.IntegerField( blank=True, null=True)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)
    renuncia = models.ForeignKey(Renuncia, on_delete=models.PROTECT, blank=True, null=True)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT) 
    requerimiento_trabajador = models.ForeignKey(RequerimientoTrabajador, on_delete=models.PROTECT)
    causal = models.ForeignKey(Causal, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.trabajador.rut) + '-' + str(self.id).zfill(4)
    
    def toJSON(self):
        item = model_to_dict(self) 
        item['archivo'] = str(self.archivo).zfill(0) 
        item['requerimiento'] = self.requerimiento_trabajador.requerimiento.nombre.title() + "<br> Planta : " + self.planta.nombre.title()
        # item['requerimiento'] = "Planta : " + self.planta.nombre.title()
        item['contrato'] = "Tipo: " + self.contrato.tipo_documento.nombre.title() + "<br> Causal: " + self.causal.nombre.title() + "<br> Motivo:  " + self.contrato.motivo + "<br> Jornada:  " + self.contrato.horario.nombre.title()
        # item['contrato'] = "Tipo: " + self.contrato.tipo_documento.nombre.title() + "<br> Causal: " + self.causal.nombre.title() + "<br> Motivo:  " + self.motivo + "<br> Jornada:  " + self.contrato.horario.nombre.title() + "<br> Renta:  " + str(self.nueva_renta)
        item['trabajador'] = self.trabajador.first_name.title() + " " + self.trabajador.last_name.title() + "<br>" + self.trabajador.rut + "<br>" + self.trabajador.email
        item['nombre'] = self.trabajador.first_name.title() + " " + self.trabajador.last_name.title()
        item['plazos'] = "Fecha Inicio: "+ str(self.fecha_inicio.strftime('%d-%m-%Y')) + "<br> Fecha Termino:  " + str(self.fecha_termino.strftime('%d-%m-%Y'))    
        item['solicitante'] = self.created_by.first_name.title() + " " + self.created_by.last_name.title()
        return item


def contrato_directory_path(instance, filename):
    return '/'.join(['contratos', str(instance.contrato.trabajador.id), filename])


class Finiquito(BaseModel):
    total_pagar = models.IntegerField(default=0)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el finiquito, deshabilite esta casilla.'
    )
   
    def __str__(self):
        return str(self.total_pagar)


class ContratosEquipo(BaseModel):
    cantidad = models.IntegerField(default=0)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el los equipos de este contrato, deshabilite esta casilla.'
    )
    
    def __str__(self):
        return str(self.cantidad)


class Revision(BaseModel):

    PENDIENTE = 'PD'
    APROBADO = 'AP'
    RECHAZADO ='RC'
  

    ESTADO = (
        (PENDIENTE, 'Pendiente'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO,'Rechazado'),
    )
    obs = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=2, choices=ESTADO, default=PENDIENTE)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, null=True, blank=True)
    anexo = models.ForeignKey(Anexo, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el los equipos de este contrato, deshabilite esta casilla.'
    )
    def __str__(self):
        return self.obs


class MotivoBaja(BaseModel):
    """Modelo Motivo baja.
    """
    nombre = models.CharField(max_length=250, unique=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el Motivo, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre


class Baja(BaseModel):

    PENDIENTE = 'PD'
    APROBADO = 'AP'
    RECHAZADO ='RC'
  

    ESTADO = (
        (PENDIENTE, 'Pendiente'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO,'Rechazado'),
    )
    motivo = models.ForeignKey(MotivoBaja, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADO, default=PENDIENTE)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, null=True, blank=True)
    anexo = models.ForeignKey(Anexo, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el los equipos de este contrato, deshabilite esta casilla.'
    )
    def __str__(self):
        return str(self.motivo)
    
    def toJSON(self):
        item = model_to_dict(self)
        if(self.contrato): 
            item['archivo'] = str(self.contrato.archivo).zfill(0)
        else:
            item['archivo'] = str(self.anexo.archivo).zfill(0)

        if(self.contrato):
            if(self.contrato.valores_diario):
                item['contrato'] = "Tipo: " + str(self.contrato.tipo_documento.nombre.title()) + " <br> Causal : " + str(self.contrato.causal.nombre.title()) + "<br> Motivo:  " + str(self.contrato.motivo) + "<br> Jornada:  " + str(self.contrato.horario.nombre.title()) + "<br> Renta:  " + str(self.contrato.valores_diario.valor_diario)
            elif(self.contrato.sueldo_base):
                item['contrato'] = "Tipo: " + str(self.contrato.tipo_documento.nombre.title() )+  "<br> Causal : " + str(self.contrato.causal.nombre.title()) + "<br> Motivo:  " + str(self.contrato.motivo) + "<br> Jornada:  " + str(self.contrato.horario.nombre.title()) + "<br> Renta:  " + str(self.contrato.sueldo_base)
        else:
            item['contrato'] = ''
        
        if(self.contrato):     
            item['requerimiento'] = "Planta : " + str(self.contrato.planta.nombre.title())
        else:     
            item['requerimiento'] = "Planta : " + str(self.anexo.planta.nombre.title())

        if(self.contrato):
            item['trabajador'] = self.contrato.trabajador.first_name.title() + " " + self.contrato.trabajador.last_name.title() + "<br>" + self.contrato.trabajador.rut + "<br>" + self.contrato.trabajador.email
        else:
            item['trabajador'] = self.anexo.trabajador.first_name.title() + " " + self.anexo.trabajador.last_name.title() + "<br>" + self.anexo.trabajador.rut + "<br>" + self.anexo.trabajador.email

        if(self.contrato):
            item['nombre'] = self.contrato.trabajador.first_name.title() + " " + self.contrato.trabajador.last_name.title()
        else:
            item['nombre'] = self.anexo.trabajador.first_name.title() + " " + self.anexo.trabajador.last_name.title()

        if(self.contrato):
            item['plazos'] = "Fecha Inicio: "+ str(self.contrato.fecha_inicio.strftime('%d-%m-%Y')) + "<br> Fecha Termino:  " + str(self.contrato.fecha_termino.strftime('%d-%m-%Y'))
        else:
            item['plazos'] = "Fecha Inicio: "+ str(self.anexo.fecha_inicio.strftime('%d-%m-%Y')) + "<br> Fecha Termino:  " + str(self.anexo.fecha_termino.strftime('%d-%m-%Y'))

        if(self.contrato):    
            item['solicitante'] = self.contrato.created_by.first_name.title() + " " + self.contrato.created_by.last_name.title()
        else:    
            item['solicitante'] = self.anexo.created_by.first_name.title() + " " + self.anexo.created_by.last_name.title()
        item['motivo'] = self.motivo.nombre
        if(self.contrato):
            item['id_contrato'] =  self.contrato.id
        else:
            item['id_contrato'] =  self.anexo.id

        return item

        
class TemporalContratoDia(BaseModel):
    """Modelo temporal contrato dia .
    """

    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, null=True, blank=True)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT)
    numero_contrato = models.IntegerField(default=0)
    numero_proceso = models.IntegerField(default=0)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el Motivo, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.numero_contrato


class ContratosParametrosGen(BaseModel):
    """Modelo Contratos Parametros Gen .
    """

    codigo_empresa   = models.IntegerField(default=1)
    contrato_tipo  = models.IntegerField(default=1)
    umbral_fechainicio  = models.IntegerField(default=1)
    rut_firmante = models.CharField(
        max_length=12,
        unique=True,
        error_messages={
            'unique': 'Ya existe un rut firmante con este RUT registrado.'
        }
    )
    rut_empresa = models.CharField(
        max_length=12,
        unique=True,
        error_messages={
            'unique': 'Ya existe un rut empresa con este RUT registrado.'
        }
    )
    hora_dia  = models.IntegerField(default=1)
    imponible_legal = models.FloatField()
    factor_gratificacion = models.FloatField()
    dias_causal_a  = models.IntegerField(default=1)
    dias_causal_b  = models.IntegerField(default=1)
    dias_causal_c  = models.IntegerField(default=1)
    dias_causal_d  = models.IntegerField(default=1)
    dias_causal_e  = models.IntegerField(default=1)
    dias_causal_f  = models.IntegerField(default=1)
    dias_contrato_dia  = models.IntegerField(default=1)
    ruta_documentos =  models.CharField(max_length=60,
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el Motivo, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.codigo_empresa
