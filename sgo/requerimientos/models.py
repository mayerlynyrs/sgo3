from django.db import models

# Create your models here.
"""Django models requerimientos."""

import os
# Django
from django.utils import timezone
from django.forms import model_to_dict
#Utilities
from utils.models import BaseModel, Planta, Area, Cargo, Cliente
#User
from users.models import User


class Causal(models.Model):
    """Modelo Causal.
    """
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField()
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la causal, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre


class Requerimiento(BaseModel):
    """Requerimiento Model


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
        max_length=8,
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

    fecha_termino = models.DateField(null=True, blank=True)

    fecha_adendum = models.DateField(null=True, blank=True)

    descripcion = models.TextField(
        'Descripción',
        blank=True,
        null=True
    )

    motivo = models.TextField(
        'Motivo',
        blank=True,
        null=True
    )

    bloqueo = models.BooleanField(
        default=False,
        help_text='Para bloquear el requerimiento, habilite esta casilla.'
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el requerimiento, deshabilite esta casilla.'
    )

    causal = models.ForeignKey(Causal, on_delete=models.PROTECT, null=True, blank=True)
    planta = models.ForeignKey(Planta, related_name="reque_requerimiento_planta", on_delete=models.PROTECT, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, related_name="reque_requerimiento_cliente", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.nombre
        item['cliente_id'] = self.cliente.id
        item['cliente'] = self.cliente.abreviatura
        return item


class AreaCargo(BaseModel):
    """AreaCargo Model


    """

    cantidad = models.IntegerField(
        blank=True,
        null=True
    )

    valor_aprox = models.FloatField(
        blank=True,
        null=True
    )

    fecha_ingreso = models.DateField(null=True, blank=True)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el area cargo, deshabilite esta casilla.'
    )

    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, null=True, blank=True)

    area = models.ForeignKey(Area, on_delete=models.PROTECT, null=True, blank=True)

    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.cantidad) +' '+ self.area.nombre +' - '+ self.cargo.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['area'] = self.area.nombre
        item['area_id'] = self.area.id
        item['cargo'] = self.cargo.nombre
        item['cargo_id'] = self.cargo.id
        # item['region_id'] = self.region.id
        # item['provincia_id'] = self.provincia.id
        # item['bono'] =  [t.toJSON() for t in self.bono.all()]
        # item['examen'] = [t.toJSON() for t in self.examen.all()]
        return item


class RequerimientoUser(BaseModel):
    """RequerimientoUser Model


    """
    SUPERVISOR = 'SUP'
    TECNICO = 'TEC'

    TIPO_ESTADO = (
        (SUPERVISOR, 'Supervisor'),
        (TECNICO, 'Técnico'),
    )

    referido = models.BooleanField(
        default=False,
        help_text='Para marcar como referido, habilite esta casilla.'
    )

    descripcion = models.TextField(
        'Descripción',
        blank=True,
        null=True
    )

    tipo = models.CharField(max_length=3, choices=TIPO_ESTADO, default=TECNICO)

    jefe_area = models.ForeignKey(User, related_name='jefearea_requerimientouser_set', on_delete=models.PROTECT, null=True, blank=True)

    pension = models.IntegerField(
        blank=True,
        null=True
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el requerimiento del usuario, deshabilite esta casilla.'
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, null=True, blank=True)

    area_cargo = models.ForeignKey(AreaCargo, on_delete=models.PROTECT, null=True, blank=True)

    # bateria = models.ForeignKey(Bateria, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.tipo) + ' ' + str(self.user)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['user_id'] = self.user.id
        item['user_rut'] = self.user.rut
        item['user'] = self.user.first_name +' '+ self.user.last_name
        item['jefe_area_id'] = self.jefe_area.id
        item['jefe_area'] = self.jefe_area.first_name
        item['area_cargo_id'] = self.area_cargo.id
        item['area_cargo'] = '('+ str(self.area_cargo.cantidad) +') '+ self.area_cargo.area.nombre +' - '+ self.area_cargo.cargo.nombre
        item['requerimiento'] = self.requerimiento.nombre
        return item


class Adendum(BaseModel):
    """Adendum Model


    """

    fecha_inicio = models.DateField(null=True, blank=True)

    fecha_termino = models.DateField(null=True, blank=True)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el adendum, deshabilite esta casilla.'
    )

    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.fecha_termino)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_inicio'] = str(self.fecha_inicio)
        item['fecha_termino'] = str(self.fecha_termino)
        item['requerimiento_id'] = self.requerimiento.id
        item['requerimiento'] = self.requerimiento.nombre
        return item
