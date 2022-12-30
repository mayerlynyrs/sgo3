from django.utils import timezone
from django.forms import model_to_dict
from django.db import models
# Utilities
from utils.models import BaseModel
from contratos.models import Contrato, Anexo, TipoDocumento
from requerimientos.models import PuestaDisposicion 
from users.models import Trabajador

# Create your models here.


class EstadoFirma(BaseModel):
    nombre = models.CharField(max_length=50)
    status = models.BooleanField(
        default=True,
        help_text='para desactivar el estado de la firma, deshabilite esta casilla.'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        return item


class Firma(BaseModel):
    respuesta_api = models.CharField(max_length=200)
    rut_trabajador = models.CharField(max_length=13)
    estado_firma = models.ForeignKey(EstadoFirma, on_delete=models.PROTECT)
    fecha_envio = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_firma = models.DateTimeField(blank=True, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, blank=True, null=True)
    anexo = models.ForeignKey(Anexo, on_delete=models.PROTECT, blank=True, null=True)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, null=True, blank=True)
    apd = models.ForeignKey(PuestaDisposicion, on_delete=models.PROTECT, blank=True, null=True)
    # adendum = models.ForeignKey(PuestaDisposicion, on_delete=models.PROTECT, blank=True, null=True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la firma, deshabilite esta casilla.'
    )
    
    def __str__(self):
        return self.respuesta_api
    
    def toJSON(self):
        item = model_to_dict(self)
        item['rut_trabajador'] = self.rut_trabajador
        item['estado_firma'] = self.estado_firma
        item['contrato_id'] =  self.contrato.id
        item['apd_id'] =  self.apd.id
        return item


class Api(models.Model):
    # Resultados
    identif_evidencia = models.CharField('ID de evidencia', max_length=200)
    asunto = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    resultado = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    fecha_procesado = models.DateTimeField(blank=True, null=True)
    fecha_enviado = models.DateTimeField(blank=True, null=True)
    fecha_cerrado = models.DateTimeField(blank=True, null=True)
    fecha_firmado = models.DateTimeField(blank=True, null=True)
    fecha_rechazado = models.DateTimeField(blank=True, null=True)
    # Partes firmantes (2)
    identif_partido_trab = models.CharField('ID de partido Trabajador', max_length=200)
    nombre_trab = models.CharField(max_length=200)
    correo_trab = models.CharField(max_length=200)
    identif_partido_empl = models.CharField('ID de partido Empleado', max_length=200)
    nombre_empl = models.CharField(max_length=200)
    correo_empl = models.CharField(max_length=200)
    metodo_firma = models.CharField(max_length=200)
    firma = models.ForeignKey(Firma, on_delete=models.PROTECT)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el registro de la api, deshabilite esta casilla.'
    )
    
    def __str__(self):
        return self.asunto
    
    def toJSON(self):
        item = model_to_dict(self)
        item['estado'] = self.estado
        item['resultado'] = self.resultado
        item['firma_id'] =  self.firma.id
        return item


class DocApi(models.Model):
    # affidavits (declaraciones juradas)
    identif_unica = models.CharField('ID único', max_length=200)
    fecha = models.DateTimeField(blank=True, null=True)
    identif_unica_evidencia = models.CharField('ID único evidencia', max_length=200)
    identif_unica_partido = models.CharField('ID único partido', max_length=200)
    b64 = models.TextField(blank=True, null=True)
    descripcion = models.CharField(max_length=200)
    api = models.ForeignKey(Api, on_delete=models.PROTECT)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar documentos de la api, deshabilite esta casilla.'
    )
    
    def __str__(self):
        return self.descripcion
    
    def toJSON(self):
        item = model_to_dict(self)
        item['identif_unica'] = self.identif_unica
        item['descripcion'] = self.descripcion
        item['api_id'] =  self.api.id
        return item
