from xml.dom import ValidationErr
from django.db import models

# Create your models here.
"""Django models examenes."""

import os
# Django
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.forms import model_to_dict
#Utilities
from utils.models import BaseModel, Planta
#Requerimientos
from requerimientos.models import RequerimientoUser
#User
from users.models import User


class Examen(models.Model):
    """Modelo Examen.
    """
    nombre = models.CharField(max_length=250)
    valor = models.IntegerField()
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el examen, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

class Bateria(models.Model):
    """Modelo Bateria.
    """


    nombre = models.CharField(max_length=250)
    examen = models.ManyToManyField(
        Examen,
        related_name="examenes",
        help_text='Seleccione uno o mas exámenes para esta bateria.'
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la bateria de examenes, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre
        # return self.nombre + '-' + self.examen.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['examen'] = [t.toJSON() for t in self.examen.all()]
        # item['examen'] = [model_to_dict(t) for t in self.examen.all()]
        return item


class Evaluacion(BaseModel):
    """Evaluacion Model


    """
    APROBADO = 'A'
    RECHAZADO = 'R'
    EVALUADO = 'E'

    RESULTADOS_ESTADO = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (EVALUADO, 'Evaluado'),
    )

    nombre = models.CharField(
        max_length=120,
    )

    fecha_examen = models.DateField(null=True, blank=True)

    fecha_vigencia = models.DateField(null=True, blank=True)

    descripcion = models.TextField(
        'Descripción',
        blank=True,
        null=True
    )

    valor_examen = models.IntegerField(
        blank=True,
        null=True
    )

    referido = models.BooleanField(
        default=False,
        help_text='Para marcar como referido, habilite esta casilla.'
    )

    resultado = models.CharField(max_length=1, choices=RESULTADOS_ESTADO, default=EVALUADO)

    archivo = models.FileField(
        upload_to='resultadosexamenes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])]
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el requerimiento, deshabilite esta casilla.'
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    examen = models.ForeignKey(Examen, on_delete=models.PROTECT, null=True, blank=True)

    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['archivo'] = str(self.archivo).zfill(0)
        item['examen'] = self.examen.nombre
        item['examen_id'] = self.examen.id
        item['resultado'] = self.resultado
        return item


class Requerimiento(BaseModel):
    """Requerimiento Model


    """
    APROBADO = 'A'
    RECHAZADO = 'R'

    ESTADOS = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
    )

    fecha_inicio = models.DateField(null=True, blank=True)

    fecha_termino = models.DateField(null=True, blank=True)

    estado = models.CharField(max_length=1, choices=ESTADOS, default=RECHAZADO)

    resultado = models.CharField(
        max_length=120,
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el requerimiento del usuario, deshabilite esta casilla.'
    )

    requerimiento_user = models.ForeignKey(RequerimientoUser, related_name="exam_requer_user", on_delete=models.PROTECT, null=True, blank=True)

    examen = models.ForeignKey(Examen, on_delete=models.PROTECT, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    planta = models.ForeignKey(Planta, related_name="exam_requerimiento_planta", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.resultado


