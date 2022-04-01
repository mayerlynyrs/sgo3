"""Profesiones model."""

# Django
from django.db import models
from django.utils import timezone

from django.forms import model_to_dict


class Especialidad(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la especialidad, deshabilite esta casilla.'
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
        item['nombre'] = self.nombre.title()
        return item

    # class Meta:
    #     verbose_name = 'Especialidad'
    #     verbose_name_plural = 'Especialidades'
    #     ordering = ['id']
