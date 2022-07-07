"""Epps model."""

from django.db import models
from django.utils import timezone
from django.forms import model_to_dict

# Create your models here.
from clientes.models import Cliente, Planta
#Requerimientos
from requerimientos.models import BaseModel, Requerimiento, AreaCargo
from users.models import Trabajador


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


class ConvenioRequerimiento(BaseModel):
    """ConvenioRequerimiento Model


    """

    convenio = models.ForeignKey(Convenio, on_delete=models.PROTECT, null=True, blank=True)

    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, null=True, blank=True)

    area_cargo = models.ForeignKey(AreaCargo, verbose_name='Área Cargo', on_delete=models.PROTECT, null=True, blank=True)

    # cantidad = models.IntegerField(
    #     blank=True,
    #     null=True
    # )

    valor_total = models.BigIntegerField(
        blank=True,
        null=True
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el convenio de este requerimiento, deshabilite esta casilla.'
    )

    def __str__(self):
        return str(self.valor_total)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['convenio_id'] = self.convenio.id
        item['convenio'] = self.convenio.nombre
        item['convenio_insumo'] =  [t.toJSON() for t in self.convenio.insumo.all()]
        item['area_cargo_id'] = self.area_cargo.id
        item['area_cargo'] = '('+ str(self.area_cargo.cantidad) +') ' + ' / '+ self.area_cargo.area.nombre + ' - '+ self.area_cargo.cargo.nombre
        item['a_c'] = self.area_cargo.area.nombre + ' - '+ self.area_cargo.cargo.nombre
        item['requerimiento_id'] = self.requerimiento.id
        item['requerimiento'] = self.requerimiento.nombre
        return item


class ConvenioRequerTrabajador(BaseModel):
    """ConvenioRequerTrabajador Model


    """

    convenio = models.ForeignKey(Convenio, on_delete=models.PROTECT, null=True, blank=True)

    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, null=True, blank=True)

    area_cargo = models.ForeignKey(AreaCargo, verbose_name='Área Cargo', on_delete=models.PROTECT, null=True, blank=True)

    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, null=True, blank=True)

    estado = models.BooleanField(
        help_text='Para confirmar True, para anular False.'
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el convenio requerimiento de este trabajador, deshabilite esta casilla.'
    )

    def __str__(self):
        return str(self.id)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['convenio_id'] = self.convenio.id
        item['convenio'] = self.convenio.nombre
        item['area_cargo_id'] = self.area_cargo.id
        item['area_cargo'] = '('+ str(self.area_cargo.cantidad) +') ' + ' - '+ self.area_cargo.cargo.nombre
        item['requerimiento_id'] = self.requerimiento.id
        item['requerimiento'] = self.requerimiento.nombre
        item['trabajador_id'] = self.trabajador.id
        item['trabajador'] = self.trabajador.first_name +" "+self.trabajador.last_name
        return item
