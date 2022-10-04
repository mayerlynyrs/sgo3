from django.utils import timezone
from django.forms import model_to_dict
from django.db import models
# Utilities
from utils.models import BaseModel

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
        return item