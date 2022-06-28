"""Epps model."""

from django.db import models
from django.utils import timezone
from django.forms import model_to_dict

# Create your models here.
from clientes.models import Cliente, Planta


class TipoInsumo(models.Model):
    nombre = models.CharField(max_length=50)
    status = models.BooleanField(
        default=True,
        help_text='para desactivar el tipo de Insumo, deshabilite esta casilla.'
    )

    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        return item


class Insumo(models.Model):
    codigo_externo = models.CharField('Código Externo', max_length=20)
    nombre = models.CharField(max_length=100)
    costo = models.FloatField()
    tipo_insumo = models.ForeignKey(TipoInsumo, on_delete=models.CASCADE)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el insumo, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
        default= timezone.now,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['codigo_externo'] = self.codigo_externo
        item['nombre'] = self.nombre.title()
        item['tipo_insumo_id'] = self.tipo_insumo.id
        item['tipo_insumo'] = self.tipo_insumo.nombre.title()
        return item


class Convenio(models.Model):
    nombre = models.CharField(max_length=50)
    valor = models.FloatField()
    validez = models.IntegerField()
    
    insumo = models.ManyToManyField(
        Insumo,
        help_text='Seleccione uno o mas insumos para este convenio.')

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )
    planta = models.ForeignKey(
        Planta,
        on_delete=models.CASCADE
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el convenio, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
        default= timezone.now,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['insumo'] =  [t.toJSON() for t in self.insumo.all()]
        item['cliente_id'] = self.cliente.id
        item['cliente'] = self.cliente.razon_social.title()
        item['planta_id'] = self.planta.id
        item['planta'] = self.planta.nombre.title()
        return item
