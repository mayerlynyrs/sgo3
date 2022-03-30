"""Contratos model."""
import os

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import FileExtensionValidator
# Models
from users.models import User
# Clientes
from clientes.models import Planta
# Utilities
from utils.models import BaseModel, Bono, Equipo, Gratificacion, Horario
from contratos.models import TipoDocumento
from requerimientos.models import RequerimientoUser, Causal

User = get_user_model()

class Renuncia(BaseModel):
    nombre = models.CharField(max_length=250)
    archivo = models.FileField(
        upload_to='renuncias/',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', ])]
    )
    fecha_termino = models.DateField(blank=True, null=True)
    requerimiento_user = models.ForeignKey(RequerimientoUser, on_delete=models.PROTECT)
    
    
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el bono, deshabilite esta casilla.'
    )
    
    def __str__(self):
        return self.nombre


class Contrato(BaseModel):
    POR_FIRMAR = 'PF'
    FIRMADO_TRABAJADOR = 'FT'
    FIRMADO_EMPLEADOR = 'FE'
    FIRMADO = 'FF'
    OBJETADO = 'OB'

    CREADO = 'CR'
    PROCESO_VALIDACION = 'PV'
    APROBADO = 'AP'
    PENDIENTE_BAJA ='PB'
    BAJADO = 'BJ'

    DIARIO = 'D'
    MENSUAL = 'M'
    MENSUAL30 = 'M3'

    FIRMA_ESTADO = (
        (POR_FIRMAR, 'Por Firmar'),
        (FIRMADO_TRABAJADOR, 'Firmado por Trabajador'),
        (FIRMADO_EMPLEADOR, 'Firmado por Empleador'),
        (FIRMADO, 'Firmado'),
        (OBJETADO, 'Objetado'),
    )

    CONTRATO_ESTADO = (
        (CREADO, 'Creado'),
        (PROCESO_VALIDACION, 'en Proceso de  Validacion'),
        (APROBADO, 'Aprobado'),
        (PENDIENTE_BAJA,'en Proceso de baja'),
        (BAJADO,'Bajado'),
    )

    TIPO_CONTRATO = (
        (DIARIO, 'Diario'),
        (MENSUAL, 'Mensual'),
        (MENSUAL30, 'Mensual 30 hrs'),
    )

    sueldo_base = models.IntegerField(default=0)
    fecha_pago = models.DateField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=False, null=False)
    fecha_termino = models.DateField(blank=False, null=False)
    fecha_termino_ultimo_anexo = models.DateField(blank=True, null=True)
    archivo = models.FileField(
        upload_to='contratoscreados/',
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])]
    )
    motivo = models.TextField(blank=True, null=True)
    archivado = models.BooleanField(default=False)
    tipo_contrato = models.CharField(max_length=2, choices=TIPO_CONTRATO, default=MENSUAL)
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
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    gratificacion = models.ForeignKey(Gratificacion, on_delete=models.PROTECT)
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT)
    renuncia = models.ForeignKey(Renuncia, on_delete=models.PROTECT, blank=True, null=True)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT) 
    requerimiento_user = models.ForeignKey(RequerimientoUser, on_delete=models.PROTECT)
    causal = models.ForeignKey(Causal, on_delete=models.PROTECT)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el contrato , deshabilite esta casilla.'
    )
    def __str__(self):
        return str(self.user.rut) + '-' + str(self.id).zfill(4)


def contrato_directory_path(instance, filename):
    return '/'.join(['contratos', str(instance.contrato.user.id), filename])

class Anexo(BaseModel):
    POR_FIRMAR = 'PF'
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
        upload_to='anexoscreados/',
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
    
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)
    renuncia = models.ForeignKey(Renuncia, on_delete=models.PROTECT)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT) 
    requerimiento_user = models.ForeignKey(RequerimientoUser, on_delete=models.PROTECT)
    causal = models.ForeignKey(Causal, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.user.rut) + '-' + str(self.id).zfill(4)


def contrato_directory_path(instance, filename):
    return '/'.join(['contratos', str(instance.contrato.user.id), filename])

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
        return str(self.contrato.user) + '-' + self.nombre_archivo

    @property
    def nombre_archivo(self):
        return os.path.basename(self.archivo.name)


class ContratosBono(models.Model):
    valor = models.IntegerField(default=0)
    descripcion = models.TextField('Descripción')
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
        return self.nombre


class Finiquito(BaseModel):
    total_pagar = models.IntegerField(default=0)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el finiquito, deshabilite esta casilla.'
    )
   
    def __str__(self):
        return self.nombre

class ContratosEquipo(BaseModel):
    cantidad = models.IntegerField(default=0)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el los equipos de este contrato, deshabilite esta casilla.'
    )
    
    def __str__(self):
        return self.nombre

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
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    anexo = models.ForeignKey(Anexo, on_delete=models.CASCADE)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el los equipos de este contrato, deshabilite esta casilla.'
    )
    def __str__(self):
        return self.nombre

    