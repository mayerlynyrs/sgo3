from django.db import models

# Create your models here.
"""Django models requerimientos."""

import os
# Django
from django.core.validators import FileExtensionValidator
#Utilities
from utils.models import BaseModel, Cliente, Negocio, Planta
#User
from users.models import Especialidad


class Requerimiento(BaseModel):
    """Requerimiento Model

    El objeto Requerimiento tiene los siguientes atributos:
        + nombre (char): Nombre del Requerimiento
        + desc (text): Descripcion del Requerimiento
        + url (file): Atributo con la referencia al achivo
        + negocios (manytomany): Las negocios que pueden visualizar este requerimiento.
        + status (boolean): Estado del Requerimiento.
    """
    NORMAL = 'NOR'
    PARADA_GENERAL_PLANTA = 'PGP'
    URGENCIA = 'URG'

    REGIMEN_ESTADO = (
        (NORMAL, 'Normal'),
        (PARADA_GENERAL_PLANTA, 'Parada Planta'),
        (URGENCIA, 'Urgencia'),
    )

    codigo = models.CharField(
        'código',
        help_text='Identificador único de sistema de gestión.',
        max_length=6,
        unique=True,
        blank=True,
        null=True
    )

    centro_costo = models.CharField(
        max_length=120,
    )

    nombre = models.CharField(
        max_length=120,
    )

    fecha_solicitud = models.DateField(null=True, blank=True)

    regimen = models.CharField(max_length=3, choices=REGIMEN_ESTADO, default=NORMAL)

    fecha_inicio = models.DateField(null=True, blank=True)

    fecha_fin = models.DateField(null=True, blank=True)

    fecha_adendum = models.DateField(null=True, blank=True)

    comentario = models.TextField(
        'Comentario',
        blank=True,
        null=True
    )

    motivo = models.TextField(
        'Motivo',
        blank=True,
        null=True
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el requerimiento, deshabilite esta casilla.'
    )

    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.nombre

    @property
    def nombre_url(self):
        return os.path.basename(self.url.name)

    @property
    def extension_url(self):
        name, extension = os.path.splitext(self.url.name)
        return extension
