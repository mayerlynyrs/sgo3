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
    
    def toJSON(self):
        item = model_to_dict(self)
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

    requerimiento_user = models.ForeignKey(RequerimientoUser, on_delete=models.PROTECT, null=True, blank=True)

    examen = models.ForeignKey(Examen, on_delete=models.PROTECT, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    planta = models.ForeignKey(Planta, related_name="exam_requerimiento_planta", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.resultado


class Psicologico(models.Model):
    """Psicologico Model


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
        help_text='Para desactivar el examen psicologico, deshabilite esta casilla.'
    )

    requerimiento_user = models.ForeignKey(RequerimientoUser, on_delete=models.PROTECT, null=True, blank=True)

    examen = models.ForeignKey(Examen, on_delete=models.PROTECT, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, null=True, blank=True)

    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.resultado


class PsicologicoTipo(models.Model):
    """Modelo Psicologico Tipo.
    """


    nombre = models.CharField(max_length=250)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar tipo de examenes psicologico, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre


class EvaluacionPsicologico(models.Model):
    """Evaluacion Psicologico Model


    """
    ESPERA_EVALUACION = 'E'
    APROBADO = 'A'
    RECHAZADO = 'R'

    ESTADOS = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (ESPERA_EVALUACION, 'Espera evaluacion'),
    )

    nombre = models.CharField(max_length=250)

    estado = models.CharField(max_length=1, choices=ESTADOS, default=ESPERA_EVALUACION)

    fecha_inicio = models.DateField(null=True, blank=True)

    fecha_termino = models.DateField(null=True, blank=True)

    resultado = models.CharField(
        max_length=120,
    )

    archivo = models.FileField(
        upload_to='evaluacionpsicologica/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])]
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la evaluacion del examen psicologico, deshabilite esta casilla.'
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    psicologico_tipo = models.ForeignKey(PsicologicoTipo, on_delete=models.PROTECT, null=True, blank=True)

    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.resultado

class Agenda(BaseModel):
    """Agendar Psicologico Model


    """
    ESPERA_EVALUACION = 'E'
    APROBADO = 'A'
    RECHAZADO = 'R'
    AGENDADO = 'AG'
    SUPERVISOR = 'SUP'
    TECNICO = 'TEC'

    TIPO_ESTADO = (
        (SUPERVISOR, 'Supervisor'),
        (TECNICO, 'Técnico'),
    )

    ESTADOS = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (ESPERA_EVALUACION, 'Espera evaluacion'),
        (AGENDADO, 'Agendado'),
    )

    tipo = models.CharField(max_length=3, choices=TIPO_ESTADO, default=TECNICO)
    referido = models.BooleanField(
        default=False,
        help_text='Para marcar como referido, habilite esta casilla.'
    )
    Hal2 = models.BooleanField(
        default=False,
        help_text='Si examen hal2 es requerido , habilite esta casilla.'                          
    )
    fecha_ingreso_estimada = models.DateField(blank=True, null=True)
    fecha_agenda_evaluacion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, default=ESPERA_EVALUACION)
    obs = models.TextField(blank=True, null=True)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la evaluacion del examen psicologico, deshabilite esta casilla.'
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, null=True, blank=True)
    evaluacion = models.ForeignKey(EvaluacionPsicologico, on_delete=models.PROTECT, null=True, blank=True)


    def __str__(self):
        return self.resultado