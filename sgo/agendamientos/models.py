"""agendamientos model."""
import os

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.forms import model_to_dict
# Models
from users.models import Trabajador
# Clientes
from clientes.models import Planta
# Utilities
from utils.models import BaseModel, Cargo
from examenes.models import Bateria, CentroMedico
from requerimientos.models import Requerimiento

User = get_user_model()

class Agendamiento(BaseModel):
    """Agendar  Model
    """
    ESPERA_EVALUACION = 'E'
    APROBADO = 'A'
    RECHAZADO = 'R'
    AGENDADO = 'AG'
    TECNICO = 'TEC'
    SUPERVISOR = 'SUP'
    PSICOLOGICA = 'PSI'
    GENERAL = 'GEN'

    TIPO_ESTADO = (
        (TECNICO, 'Técnico'),
        (SUPERVISOR, 'Supervisor'),
        
    )
    ESTADOS = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (ESPERA_EVALUACION, 'Espera de Evaluación'),
        (AGENDADO, 'Agendado'),
    )

    TIPO_EV=(
        (PSICOLOGICA, 'Psicólogia'),
        (GENERAL,'General')
    )
    tipo = models.CharField(max_length=3, choices=TIPO_ESTADO, default=TECNICO)
    tipo_evaluacion = models.CharField(max_length=3, choices=TIPO_EV)
    referido = models.BooleanField(
        default=False,
        help_text='Para marcar como referido, habilite esta casilla.'
    )
    hal2 = models.BooleanField(
        default=False,
        help_text='Si examen hal2 es requerido , habilite esta casilla.'                          
    )
    fecha_ingreso_estimada = models.DateField(blank=True, null=True)
    fecha_agenda_evaluacion = models.DateTimeField('Fecha Evaluación', blank=True, null=True,)
    estado = models.CharField(max_length=2, choices=ESTADOS, default=ESPERA_EVALUACION)
    obs = models.TextField(blank=True, null=True)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, null=True, blank=True)
    psico = models.ForeignKey(User, related_name='pisco', on_delete=models.PROTECT, null=True, blank=True)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, null=True, blank=True)
    centro = models.ForeignKey(CentroMedico, on_delete=models.PROTECT, null=True, blank=True)
    bateria = models.ForeignKey(Bateria, on_delete=models.PROTECT, null=True, blank=True)
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, null=True, blank=True)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la evaluación del examen psicólogico, deshabilite esta casilla.'
    )

    
    def __str__(self):
        return self.obs
    
    def toJSON(self):
        item = model_to_dict(self)
        if (self.fecha_agenda_evaluacion):
            item['fecha_agenda_evaluacion'] = self.fecha_agenda_evaluacion.strftime('%Y-%m-%d %H:%M')
        else:
            item['fecha_agenda_evaluacion'] = "No Asignada"
        if (self.psico):
            item['psicologo'] = self.psico.first_name +" "+self.psico.last_name
        else:
            item['psicologo'] = "No Asignado"
        if (self.tipo_evaluacion == 'PSI'):
            tipoeva = 'Psicologico'
        else:
            tipoeva = 'General'
        if (self.centro):
            item['centromedico'] = self.centro.nombre
        else:
            item['centromedico'] = "No Asignado"

        item['user_id'] = self.trabajador.id
        item['user'] = self.trabajador.first_name +" "+self.trabajador.last_name
        item['user_ciudad'] = self.trabajador.ciudad.nombre
        item['user_telefono'] = self.trabajador.telefono
        item['user_email'] = self.trabajador.email
        item['user_rut'] = self.trabajador.rut
        item['user_evalua'] = self.modified_by_id
        item['planta_nombre'] = self.planta.nombre
        item['tipo_examen'] = tipoeva
        return item
