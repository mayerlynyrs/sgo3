"""Psicologos Forms"""

# Django
from django.contrib.auth.models import Group, User

from django.forms import *
from django import forms
from django.forms import inlineformset_factory, RadioSelect
from django.contrib.auth import get_user_model
from django.forms import TextInput
# sgo Model
from psicologos.models import Agenda 
from clientes.models import Planta
from utils.models import Cargo
from users.models import Trabajador
from agendamientos.models import Agendamiento
from examenes.models import Evaluacion, Requerimiento as RequerimientoExam

User = get_user_model()


class UserAgendar(forms.ModelForm):

    SUPERVISOR = 'SUP'
    TECNICO = 'TEC'

    TIPO_ESTADO = (
        (SUPERVISOR, 'Supervisor'),
        (TECNICO, 'Técnico'),
    )


    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.filter(is_active=True), required=True, label="Trabajador",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )                            
    tipo = forms.ChoiceField(choices = TIPO_ESTADO, required=True, label="Tipo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    fecha_ingreso_estimada = forms.CharField(required=True, label="Fecha Estimada Ingreso",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_examen", }))
                           
    hal2 =forms.BooleanField(required=False,label='Hal2',
                                 widget=forms.CheckboxInput(attrs={'class': "form-control-lg",
                                                              'disabled':'disabled',}))
    obs = forms.CharField (required=False, label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))
    planta = forms.ModelChoiceField(queryset=Planta.objects.filter(status=True), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.filter(status=True), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
          
    class Meta:
        model = Agenda
        fields = ("trabajador", "tipo", "referido", "Hal2", "fecha_ingreso_estimada", "fecha_agenda_evaluacion", "obs", "planta","cargo")


class AgendaPsicologos(forms.ModelForm):

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
    )

                               
    tipo = forms.ChoiceField(choices = TIPO_ESTADO, required=True, label="Tipo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    fecha_ingreso_estimada = forms.CharField(required=True, label="Fecha Estimada Ingreso",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_ingreso", }))
                                 
    fecha_agenda_evaluacion = forms.CharField(required=True, label="Fecha Evaluacion",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_evaluacion"}))
    obs = forms.CharField (label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))
    planta = forms.ModelChoiceField(queryset=Planta.objects.filter(status=True), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.filter(status=True), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )                                
    estado = forms.ChoiceField(choices = ESTADOS, required=True, label="Tipo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    psico = forms.ModelChoiceField(queryset=User.objects.none(), required=True, label="Evaluador",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    def __init__(self, *args, **kwargs):
        users_evaluador = kwargs.pop('users_evaluador', None)
        # print('users_evaluador', users_evaluador)
        super(AgendaPsicologos, self).__init__(*args, **kwargs)
        
        self.fields['psico'].queryset = users_evaluador

    class Meta:
        model = Agendamiento
        fields = ( "tipo", "referido", "hal2", "fecha_ingreso_estimada", "fecha_agenda_evaluacion", "obs", "planta", "estado", "cargo","psico")


class EvaluacionPsicologica(forms.ModelForm):

    RECOMENDABLE = 'R'
    NO_RECOMENDABLE = 'N'
    SUPERVISOR = 'SUP'
    TECNICO = 'TEC'

    TIPO_ESTADO = (
        (SUPERVISOR, 'Supervisor'),
        (TECNICO, 'Técnico'),
    )

    ESTADOS = (
        (RECOMENDABLE, 'Recomendable'),
        (NO_RECOMENDABLE, 'No Recomendable'),

    )
                               
    tipo = forms.ChoiceField(choices = TIPO_ESTADO, required=True, label="Tipo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )                   
    estado = forms.ChoiceField(choices = ESTADOS, required=True, label="Tipo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    fecha_inicio = forms.CharField(required=True, label="Fecha Inicio",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_ingreso", }))
    fecha_termino = forms.CharField(required=True, label="Fecha Termino",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_vigencia"}))
    resultado = forms.CharField (required=True, label="Resultado",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))
    archivo = forms.FileField(required=True, label="Archivo",
                                 widget=forms.FileInput(attrs={'class': "form-control"}))
    archivo2 = forms.FileField(required=False,label="Archivo",
                                 widget=forms.FileInput(attrs={'class': "form-control"}))                                 
    planta = forms.ModelChoiceField(queryset=Planta.objects.filter(status=True), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.filter(status=True), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )                                

    class Meta:
        model = Evaluacion
        fields = ("estado", "fecha_inicio", "fecha_termino", "resultado", "archivo", "archivo2", "planta","cargo", "referido","tipo", "hal2")


class RevisionForm(forms.ModelForm):

    APROBADO = 'A'
    RECHAZADO = 'R'

    ESTADOS = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
    )
                               
    estado = forms.ChoiceField(choices = ESTADOS, required=True, label="Estado",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )               
    obs = forms.CharField (label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control"})) 

    def __init__(self, *args, **kwargs):
        super(RevisionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RequerimientoExam
        fields = ("estado", "obs")


class ReportForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    