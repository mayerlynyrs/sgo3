from xml.dom import ValidationErr
from django.db import models

# Create your models here.
"""Django models examenes."""

import os
# Django
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.forms import model_to_dict
# Clientes
from clientes.models import BaseModel, Planta
#Requerimientos
from requerimientos.models import RequerimientoTrabajador
#User
from users.models import User, Trabajador
#Utils
from utils.models import Region, Provincia, Ciudad, Cargo
#psicologo


class Examen(models.Model):
    """Modelo Examen.
    """
    nombre = models.CharField(max_length=250, unique=True)
    valor = models.IntegerField()
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el examen, deshabilite esta casilla.'
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
        item['id'] = self.id
        return item


class Bateria(models.Model):
    """Modelo Bateria.
    """


    nombre = models.CharField(max_length=250, unique=True)
    examen = models.ManyToManyField(
        Examen,
        related_name="examenes",
        help_text='Seleccione uno o mas exámenes para esta batería.'
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la batería de exámenes, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre
        # return self.nombre + '-' + self.examen.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        item['examen'] = [t.toJSON() for t in self.examen.all()]
        # item['examen'] = [model_to_dict(t) for t in self.examen.all()]
        return item


class CentroMedico(models.Model):
    nombre = models.CharField(max_length=120)
    region = models.ForeignKey(Region, verbose_name="Región", on_delete=models.SET_NULL, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(max_length=120)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el bono, deshabilite esta casilla.'
    )

    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['region_id'] = self.region.id
        item['provincia_id'] = self.provincia.id
        item['ciudad_id'] = self.ciudad.id
        return item


class Evaluacion(models.Model):
    """Evaluacion Model

    """
    RECOMENDABLE = 'R'
    NO_RECOMENDABLE = 'N'
    SUPERVISOR = 'SUP'
    TECNICO = 'TEC'
    PSICOLOGICA = 'PSI'
    GENERAL = 'GEN'

    ESTADOS = (
        (RECOMENDABLE, 'Recomendable'),
        (NO_RECOMENDABLE, 'No Recomendable'),

    )

    TIPO_ESTADO = (
        (SUPERVISOR, 'Supervisor'),
        (TECNICO, 'Técnico'),
    )

    TIPO_EV=(
        (PSICOLOGICA, 'Psicologia'),
        (GENERAL,'General')
    )

    estado = models.CharField(max_length=1, choices=ESTADOS)
    
    valor = models.IntegerField()

    tipo_evaluacion = models.CharField(max_length=3, choices=TIPO_EV)

    tipo = models.CharField(max_length=3, choices=TIPO_ESTADO, default=TECNICO)

    fecha_inicio = models.DateField(null=True, blank=True)

    fecha_termino = models.DateField(null=True, blank=True)

    resultado = models.CharField(
        max_length=120,
    )

    archivo = models.FileField(
        upload_to='evaluacionpsicologica/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])]
    )

    archivo2 = models.FileField(
        upload_to='evaluacionpsicologica/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])],
        null=True, blank=True
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la evaluacion del examen psicologico, deshabilite esta casilla.'
    )

    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, null=True, blank=True)

    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=True, blank=True)

    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, null=True, blank=True)

    referido = models.BooleanField(
        default=False,
        help_text='Para marcar como referido, habilite esta casilla.'
    )    

    hal2 = models.BooleanField(
        default=False,
        help_text='Si examen hal2 es requerido, habilite esta casilla.'                          
    )


    psicologo = models.ForeignKey(User, related_name='psico_evaluador', on_delete=models.PROTECT, null=True, blank=True)
    centro = models.ForeignKey(CentroMedico, on_delete=models.PROTECT, null=True, blank=True)
    bateria = models.ForeignKey(Bateria, verbose_name="Batería", on_delete=models.PROTECT, null=True, blank=True)

    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return str(self.fecha_inicio)

    def toJSON(self):
        item = model_to_dict(self)
        if (self.referido == True):
            estado2 = 'SI'
        else:
            estado2 = 'NO'
        if (self.tipo == 'SUP'):
            tipo = 'Supervisor'
        else:
            tipo = 'Tecnico'
        if (self.estado == 'R'):
            resultado = 'Recomendado'
        else:
            resultado = 'No Recomendado'
        if (self.psicologo):
            item['psicologo'] = self.psicologo.first_name +" "+self.psicologo.last_name
        else:
            item['psicologo'] = "No Asignado"
        if (self.centro):
            item['centromedico'] = self.centro.nombre
        else:
            item['centromedico'] = "No Asignado"
        if (self.psicologo):
            item['tipoexamen'] = "Psicologico"
        else:
            item['tipoexamen'] = "Examen General"
        
        item['resultado'] = resultado  
        item['tipo'] = tipo   
        item['referido2'] = estado2
        item['archivo'] = str(self.archivo).zfill(0)
        item['trabajador'] = self.trabajador.first_name +" "+self.trabajador.last_name
        item['trabajador_rut'] = self.trabajador.rut
        item['fecha_inicio'] = self.fecha_inicio.strftime('%d-%m-%Y')
        item['fecha_termino'] = self.fecha_termino.strftime('%d-%m-%Y')
        item['planta_nombre'] = self.planta.nombre
        item['cargo_nombre'] = self.cargo.nombre
        item['archivo2'] = ''
        return item


class Requerimiento(BaseModel):
    """Requerimiento Model


    """
    APROBADO = 'A'
    RECHAZADO = 'R'
    ENVIADO = 'E'

    ESTADOS = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (ENVIADO, 'Enviado'),
    )

    estado = models.CharField(max_length=1, choices=ESTADOS, default=RECHAZADO)

    obs = models.TextField(verbose_name="Observaciones", blank=True, null=True)

    requerimiento_trabajador = models.ForeignKey(RequerimientoTrabajador, related_name="exam_requer_trabajador", on_delete=models.PROTECT)

    bateria = models.ForeignKey(Bateria, verbose_name="Batería", on_delete=models.PROTECT, null=True, blank=True)

    psicologico = models.BooleanField(
        verbose_name="Psicológico",
        default=False,
        help_text='Si el tipo de examen psicológico es requerido, habilite esta casilla.'
    )
    
    hal2 = models.BooleanField(
        default=False,
        help_text='Si examen hal2 es requerido, habilite esta casilla.'                          
    )

    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT)

    planta = models.ForeignKey(Planta, related_name="exam_requerimiento_planta", on_delete=models.PROTECT)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el requerimiento del trabajador, deshabilite esta casilla.'
    )

    def __str__(self):
        return str(self.id)
    
    def toJSON(self):
        item = model_to_dict(self)
        if (self.psicologico):
            item['psicologico'] = "Si"
        else:
            item['psicologico'] = "No"
        if (self.hal2):
            item['hal2'] = "Si"
        else:
            item['hal2'] = "No"
        # Valida en caso de que no tengo información
        if (self.bateria):
            item['bateria'] = self.bateria.nombre.title()
            item['examen'] = [t.toJSON() for t in self.bateria.examen.all()]
        item['requerimiento_trabajador_id'] = self.requerimiento_trabajador.id
        item['trabajador_id'] = self.trabajador.id
        item['trabajador'] = self.trabajador.first_name.title() +" "+self.trabajador.last_name.title()
        item['requerimiento'] = self.requerimiento_trabajador.requerimiento.nombre.title()
        item['planta_id'] = self.planta.id
        item['planta'] = self.planta.nombre.title()
        return item
