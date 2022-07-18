from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.forms import model_to_dict
# Clientes
from clientes.models import BaseModel, Planta
from utils.models import Cargo
from users.models import User, Trabajador
from examenes.models import Examen
from requerimientos.models import RequerimientoTrabajador


class Psicologico(models.Model):
    """Psicologico Model


    """
    APROBADO = 'A'
    RECHAZADO = 'R'

    ESTADOS = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
    )

    fecha_inicio = models.DateField(null=True, blank=True)

    fecha_termino = models.DateField(null=True, blank=True)

    estado = models.CharField(max_length=1, choices=ESTADOS, default=RECHAZADO)

    resultado = models.CharField(
        max_length=120,
    )

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el examen psicologico, deshabilite esta casilla.'
    )

    requerimiento_trabajador = models.ForeignKey(RequerimientoTrabajador, on_delete=models.PROTECT, null=True, blank=True)

    examen = models.ForeignKey(Examen, on_delete=models.PROTECT, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    planta = models.ForeignKey(Planta, related_name="psicologico_planta", on_delete=models.PROTECT, null=True, blank=True)

    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.resultado



class PsicologicoTipo(models.Model):
    """Modelo Psicologico Tipo.
    """


    nombre = models.CharField(max_length=250)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar tipo de examenes psicologico, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre


class Agenda(BaseModel):
    """Agendar Psicologico Model


    """
    ESPERA_EVALUACION = 'E'
    APROBADO = 'A'
    RECHAZADO = 'R'
    AGENDADO = 'AG'
    SUPERVISOR = 'SUP'
    TECNICO = 'TEC'

    TIPO_ESTADO = (
        (SUPERVISOR, 'Supervisor'),
        (TECNICO, 'Técnico'),
    )

    ESTADOS = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (ESPERA_EVALUACION, 'Espera evaluacion'),
        (AGENDADO, 'Agendado'),
    )

    tipo = models.CharField(max_length=3, choices=TIPO_ESTADO, default=TECNICO)
    referido = models.BooleanField(
        default=False,
        help_text='Para marcar como referido, habilite esta casilla.'
    )
    Hal2 = models.BooleanField(
        default=False,
        help_text='Si examen hal2 es requerido , habilite esta casilla.'                          
    )
    fecha_ingreso_estimada = models.DateField(blank=True, null=True)
    fecha_agenda_evaluacion = models.DateTimeField(blank=True, null=True,)
    estado = models.CharField(max_length=2, choices=ESTADOS, default=ESPERA_EVALUACION)
    obs = models.TextField(blank=True, null=True)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la evaluacion del examen psicologico, deshabilite esta casilla.'
    )
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, null=True, blank=True)
    psico = models.ForeignKey(User, related_name='psicologos_evalua', on_delete=models.PROTECT, null=True, blank=True)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=True, blank=True)
    
    def __str__(self):
        return self.obs
    
    def toJSON(self):
        item = model_to_dict(self)
        if (self.fecha_agenda_evaluacion):
            item['fecha_agenda_evaluacion'] = self.fecha_agenda_evaluacion.strftime('%Y-%m-%d')
        else:
            item['fecha_agenda_evaluacion'] = "No Asignada"
        if (self.psico):
            item['psicologo'] = self.psico.first_name +" "+self.psico.last_name
        else:
            item['psicologo'] = "No Asignado"

        item['user_id'] = self.trabajador.id
        item['user'] = self.trabajador.first_name +" "+self.trabajador.last_name
        # item['user_ciudad'] = self.trabajador.ciudad.nombre
        # item['user_telefono'] = self.trabajador.telefono
        # item['user_email'] = self.trabajador.email
        item['user_rut'] = self.trabajador.rut
        item['user_evalua'] = self.modified_by_id
        return item
