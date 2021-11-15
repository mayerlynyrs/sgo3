"""Plantillas model."""

# Django
from django.db import models
from django.core.validators import FileExtensionValidator
# Mailmerge
from mailmerge import MailMerge
#Utilities
from utils.models import BaseModel, Cliente, Planta


class Tipo(BaseModel):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Plantilla(BaseModel):
    activo = models.BooleanField(default=True)
    archivo = models.FileField(
        upload_to='plantillas/',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', ])]
    )
    nombre = models.CharField(max_length=120)
    clientes = models.ManyToManyField(Cliente)
    plantas = models.ManyToManyField(Planta)
    tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

    def codigo(self):
        return str(self.pk).zfill(4)

    @property
    def atributos(self):
        documento = MailMerge(self.archivo)
        atributos = documento.get_merge_fields()
        return atributos

