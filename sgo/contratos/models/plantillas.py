"""Plantillas model."""

# Django
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.forms import model_to_dict

# Mailmerge
from mailmerge import MailMerge
# Clientes
from clientes.models import BaseModel, Cliente, Planta


class TipoDocumento(BaseModel):
    nombre = models.CharField(
                max_length = 60,
                unique = True
                )
    status = models.BooleanField(
        default=True,
        help_text='para desactivar el tipo de documento, deshabilite esta casilla.'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        return item


class Plantilla(BaseModel):
    nombre = models.CharField(max_length=120)
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)
    abreviatura = models.CharField(
                    max_length = 4,
                    unique = True
                    )
    archivo = models.FileField(
        upload_to='plantillas/',
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', ])]
    )
    clientes = models.ManyToManyField(Cliente)
    plantas = models.ManyToManyField(Planta)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def codigo(self):
        return str(self.pk).zfill(4)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        item['abreviatura'] = self.abreviatura.upper()
        return item

    @property
    def atributos(self):
        documento = MailMerge(self.archivo)
        atributos = documento.get_merge_fields()
        return atributos
