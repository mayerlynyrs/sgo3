from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.forms import model_to_dict
# Clientes
from clientes.models import BaseModel, Planta
from utils.models import Cargo
from users.models import User
from examenes.models import Examen
from requerimientos.models import RequerimientoUser


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

    requerimiento_user = models.ForeignKey(RequerimientoUser, on_delete=models.PROTECT, null=True, blank=True)

    examen = models.ForeignKey(Examen, on_delete=models.PROTECT, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, null=True, blank=True)

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


class EvaluacionPsicologico(models.Model):
    """Evaluacion Psicologico Model

    """
    RECOMENDABLE = 'R'
    NO_RECOMENDABLE = 'R'
    SUPERVISOR = 'SUP'
    TECNICO = 'TEC'

    ESTADOS = (
        (RECOMENDABLE, 'Recomendable'),
        (NO_RECOMENDABLE, 'No Recomendable'),

    )

    TIPO_ESTADO = (
        (SUPERVISOR, 'Supervisor'),
        (TECNICO, 'Técnico'),
    )

    estado = models.CharField(max_length=1, choices=ESTADOS)

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

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    referido = models.BooleanField(
        default=False,
        help_text='Para marcar como referido, habilite esta casilla.'
    )    

    Hal2 = models.BooleanField(
        default=False,
        help_text='Si examen hal2 es requerido , habilite esta casilla.'                          
    )

    psicologico_tipo = models.ForeignKey(PsicologicoTipo, on_delete=models.PROTECT, null=True, blank=True)
    psicologo = models.ForeignKey(User, related_name='psico_evaluador', on_delete=models.PROTECT, null=True, blank=True)

    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre +' '+ str(self.fecha_inicio)

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
        item['resultado'] = resultado  
        item['tipo'] = tipo   
        item['referido2'] = estado2
        item['archivo'] = str(self.archivo).zfill(0)
        item['user'] = self.user.first_name +" "+self.user.last_name
        item['psicologo'] = self.psicologo.first_name +" "+self.psicologo.last_name
        item['user_rut'] = self.user.rut
        item['fecha_inicio'] = self.fecha_inicio.strftime('%d-%m-%Y')
        item['fecha_termino'] = self.fecha_termino.strftime('%d-%m-%Y')
        item['planta_nombre'] = self.planta.nombre
        item['cargo_nombre'] = self.cargo.nombre
        return item

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
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
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

        item['user_id'] = self.user.id
        item['user'] = self.user.first_name +" "+self.user.last_name
        item['user_ciudad'] = self.user.ciudad.nombre
        item['user_telefono'] = self.user.telefono
        item['user_email'] = self.user.email
        item['user_rut'] = self.user.rut
        item['user_evalua'] = self.modified_by_id
        return item
