from django.db import models

# Create your models here.
"""Django models utilities."""

import os
# Django
# from django.db import models
from django.core.validators import FileExtensionValidator
#Utilities
from utils.models import BaseModel, Cliente, Negocio
#User
from users.models import Especialidad


class Fichero(BaseModel):
    """Fichero Model

    El objeto Fichero tiene los siguientes atributos:
        + nombre (char): Nombre del Fichero
        + desc (text): Descripcion del Fichero
        + url (file): Atributo con la referencia al achivo
        + negocios (manytomany): Las negocios que pueden visualizar este fichero.
        + status (boolean): Estado del Fichero.
    """

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la publicación de este fichero, deshabilite esta casilla.'
    )

    url = models.FileField(
        upload_to='ficheros/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])]
    )

    desc = models.TextField(
        'Descripción',
        blank=True,
        null=True
    )

    nombre = models.CharField(
        max_length=120,
    )

    clientes = models.ManyToManyField(Cliente)
    negocios = models.ManyToManyField(Negocio)

    def __str__(self):
        return self.nombre

    @property
    def nombre_url(self):
        return os.path.basename(self.url.name)

    @property
    def extension_url(self):
        name, extension = os.path.splitext(self.url.name)
        return extension


class Publicacion(BaseModel):
    """Publicacion Model

    """

    nombre = models.CharField(
        max_length=120,
    )

    descripcion = models.TextField(
        'Descripción',
        blank=True,
        null=True
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la publicación, deshabilite esta casilla.'
    )

    especialidades = models.ManyToManyField(Especialidad)

    def __str__(self):
        return self.nombre

