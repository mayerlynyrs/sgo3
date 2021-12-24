"""Profesiones model."""

# Django
from django.db import models
from django.utils import timezone
from django.forms import model_to_dict

#Users
from users.models import User


class Profesion(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la profesion, deshabilite esta casilla.'
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

class ProfesionUser(models.Model):
    egreso = models.DateField(
        null=True,
        blank=True,
        help_text="Por favor use el siguiente: <em>DD/MM/AAAA</em>."
    )
    institucion = models.CharField(
        max_length=120,
        unique=True
    )
    profesion = models.ForeignKey(Profesion, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la profesion del usuario, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.institucion
