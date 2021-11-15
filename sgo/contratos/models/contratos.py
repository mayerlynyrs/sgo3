"""Contratos model."""
import os

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
# Models
from users.models import User
# Utilities
from utils.models import BaseModel
User = get_user_model()


class Contrato(BaseModel):
    POR_FIRMAR = 'PF'
    FIRMADO_TRABAJADOR = 'FT'
    FIRMADO_EMPLEADOR = 'FE'
    FIRMADO = 'FF'
    OBJETADO = 'OB'

    CONTRATO_ESTADO = (
        (POR_FIRMAR, 'Por Firmar'),
        (FIRMADO_TRABAJADOR, 'Firmado por Trabajador'),
        (FIRMADO_EMPLEADOR, 'Firmado por Empleador'),
        (FIRMADO, 'Firmado'),
        (OBJETADO, 'Objetado'),
    )

    archivado = models.BooleanField(default=False)
    estado = models.CharField(max_length=2, choices=CONTRATO_ESTADO, default=POR_FIRMAR)
    obs = models.TextField(blank=True, null=True)

    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.usuario.rut) + '-' +str(self.id).zfill(4)


def contrato_directory_path(instance, filename):
    return '/'.join(['contratos', str(instance.contrato.usuario.id), filename])


class DocumentosContrato(BaseModel):
    archivo = models.FileField(upload_to=contrato_directory_path,
                               validators=[
                                   FileExtensionValidator(allowed_extensions=['pdf', ])])
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)

    class Meta:
        ordering = ['contrato']
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return str(self.contrato.usuario) + '-' + self.nombre_archivo

    @property
    def nombre_archivo(self):
        return os.path.basename(self.archivo.name)
