from django.db import models

# Create your models here.
"""Django models requerimientos."""

import os
# Django
from django.utils import timezone
from django.forms import model_to_dict
# Clientes
from clientes.models import Cliente, Planta
#Utilities
from utils.models import BaseModel, Area, Cargo, PuestaDisposicion
#User
from users.models import User, Trabajador


class Causal(models.Model):
    """Modelo Causal.
    """
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField('Descripción')
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
        help_text='Para desactivar el área cargo, deshabilite esta casilla.'
    )

    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, null=True, blank=True)

    area = models.ForeignKey(Area, verbose_name='Área', on_delete=models.PROTECT, null=True, blank=True)

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


class RequerimientoTrabajador(BaseModel):
    """RequerimientoTrabajador Model


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

    jefe_area = models.ForeignKey(User, verbose_name='Jefe Área', related_name='jefearea_requerimientotrabajador_set', on_delete=models.PROTECT, null=True, blank=True)

    pension = models.IntegerField(
        'Pensión',
        blank=True,
        null=True
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el requerimiento del usuario, deshabilite esta casilla.'
    )

    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, null=True, blank=True)

    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, null=True, blank=True)

    area_cargo = models.ForeignKey(AreaCargo, verbose_name='Área Cargo', on_delete=models.PROTECT, null=True, blank=True)

    # bateria = models.ForeignKey(Bateria, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.tipo) + ' ' + str(self.trabajador)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['trabajador_id'] = self.trabajador.id
        item['trabajador_rut'] = self.trabajador.rut
        item['trabajador'] = self.trabajador.first_name +' '+ self.trabajador.last_name
        item['jefe_area_id'] = self.jefe_area.id
        item['jefe_area'] = self.jefe_area.first_name
        item['area_cargo_id'] = self.area_cargo.id
        item['area_cargo'] = '('+ str(self.area_cargo.cantidad) +') '+ self.area_cargo.area.nombre +' - '+ self.area_cargo.cargo.nombre
        item['requerimiento'] = self.requerimiento.nombre
        return item


# Comienza nueva tabla Análisis Óscar
class PuestaDisposicion(BaseModel):
    """PuestaDisposicion Model


    """
    codigo_pd = models.CharField('Código', max_length=25)
    fecha_pd = models.DateField('Fecha', null=True, blank=True)
    motivo_pd = models.CharField('Motivo', max_length=200)
    fecha_inicio = models.DateField('Fecha Inicio', null=True, blank=True)
    fecha_termino = models.DateField('Fecha Término', null=True, blank=True)
    fechainicio_text = models.CharField(
        'Fecha Inicio Texto',
        max_length=200,
    )
    fechatermino_text = models.CharField(
        'Fecha Término Texto',
        max_length=200,
    )
    dias_pd = models.IntegerField('Días')
    dias_totales = models.BigIntegerField('Días Totales')
    sueldo_base = models.BigIntegerField('Sueldo Base')
    sueldo_base_gratif = models.BigIntegerField('Sueldo Base Gratif.')
    subtotal_pd = models.BigIntegerField('Subtotal')
    valor_total_pd = models.BigIntegerField('Valor Total')
    total_redondeado = models.BigIntegerField('Total Redondeado')
    total_redondeado_text = models.CharField(
        'Total Redondeado Texto',
        max_length=250,
    )
    cantidad_trabajadores = models.IntegerField()
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT)
    causal = models.ForeignKey(Causal, on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la Puesta Disposición, deshabilite esta casilla.'
    )

    def __str__(self):
        return str(self.fecha_termino)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_termino'] = str(self.fecha_termino)
        return item
# Finaliza nueva tabla Análisis Óscar        


class Adendum(BaseModel):
    """Adendum Model


    """
    # Comienza Análisis Óscar
    fecha_ad = models.DateField('Fecha', null=True, blank=True)
    motivo_ad = models.CharField(
        'Motivo',
        blank=True,
        null=True,
        max_length=200
    )
    # Finaliza Análisis Óscar
    fecha_inicio = models.DateField('Fecha Inicio', null=True, blank=True)
    fecha_termino = models.DateField('Fecha Término', null=True, blank=True)
    # Comienza Análisis Óscar
    fechainicio_text = models.CharField(
        'Fecha Inicio Texto',
        max_length=200,
        blank=True,
        null=True
    )
    fechatermino_text = models.CharField(
        'Fecha Término Texto',
        max_length=200,
        blank=True,
        null=True
    )
    dias_ad = models.BigIntegerField(
        'Días',
        blank=True,
        null=True
    )
    dias_totales_ad = models.BigIntegerField('Días Totales', null=True, blank=True)
    sueldo_base = models.BigIntegerField('Sueldo Base', null=True, blank=True)
    sueldo_base_gratif = models.BigIntegerField('Sueldo Base Gratif.', null=True, blank=True)
    subtotal_ad = models.BigIntegerField('Subtotal', null=True, blank=True)
    valor_total_pd = models.BigIntegerField('Valor Total', null=True, blank=True)
    total_redondeado_ad = models.BigIntegerField('Total Redondeado', null=True, blank=True)
    total_redondeado_ad_text = models.CharField(
        'Total Redondeado Texto',
        null=True,
        blank=True,
        max_length=250,
    )
    # Finaliza Análisis Óscar
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, null=True, blank=True)
    # Comienza Análisis Óscar
    puesta_disposicion = models.ForeignKey(PuestaDisposicion, on_delete=models.PROTECT, blank=True, null=True)
    # Finaliza Análisis Óscar

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el adendum, deshabilite esta casilla.'
    )

    def __str__(self):
        return str(self.fecha_termino)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_inicio'] = str(self.fecha_inicio)
        item['fecha_termino'] = str(self.fecha_termino)
        item['requerimiento_id'] = self.requerimiento.id
        item['requerimiento'] = self.requerimiento.nombre
        return item
