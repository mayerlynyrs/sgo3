
from django.forms import model_to_dict
from django.db import models
# Utilities
from utils.models import BaseModel

# Create your models here.


class Tipo(BaseModel):
    nombre = models.CharField(max_length=60)
    sub_tipo = models.BooleanField(
        default=False,
        help_text='para indicar "Correo y Sistema" habilite esta casilla (True), para indicar "Sistema" deshabilite esta casilla (False).'
    )
    status = models.BooleanField(
        default=True,
        help_text='para desactivar el tipo de notificación, deshabilite esta casilla.'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        return item


class Destinatario(BaseModel):
    tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
    notifica_sistema = models.CharField(max_length=250)
    fecha_notificacion = models.DateField('Fecha Notificación', blank=True, null=True)
    fecha_apertura = models.DateField(blank=True, null=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el destinatario de la notificación, deshabilite esta casilla.'
    )
    
    def __str__(self):
        return self.notifica_sistema
