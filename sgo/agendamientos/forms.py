"""Agendamiento Forms"""

# Django
from django.contrib.auth.models import Group, User

from django.forms import *
from django import forms
from django.forms import inlineformset_factory, RadioSelect
from django.contrib.auth import get_user_model
from django.forms import TextInput
# sgo Model
from agendamientos.models import Agendamiento
from clientes.models import Planta
from requerimientos.models import Requerimiento
from utils.models import Cargo
from users.models import Trabajador
from examenes.models import Bateria

User = get_user_model()


class UserAgendar(forms.ModelForm):
    TECNICO = 'TEC'
    SUPERVISOR = 'SUP'
    

    TIPO_ESTADO = (
        (TECNICO, 'Técnico'),
        (SUPERVISOR, 'Supervisor'),
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
    obs = forms.CharField (required=False, label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))
    planta = forms.ModelChoiceField(queryset=Planta.objects.filter(status=True), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.filter(status=True), required=True, label="Cargo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    
    bateria = forms.ModelChoiceField(queryset=Bateria.objects.filter(status=True), required=False, label="Batería",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true',
                                                              'disabled':'disabled',
                                                              })
                                   )
    requerimiento = forms.ModelChoiceField(queryset=Requerimiento.objects.filter(status=True), required=True, label="Requerimiento",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true',                                                            
                                                              })
                                   )
    hal2 =forms.BooleanField(required=False,label='Hal2',
                                 widget=forms.CheckboxInput(attrs={'class': "form-control-lg",
                                                              'disabled':'disabled',}))
          
    class Meta:
        model = Agendamiento
        fields = ("trabajador", "tipo", "referido", "hal2", "fecha_ingreso_estimada", "fecha_agenda_evaluacion", "obs", "planta", "cargo", "bateria", "requerimiento")




class ReportForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))


class UserAgendarSolicitud(forms.ModelForm):

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
                                                              'data-live-search-normalize': 'true',
                                                              'disabled':'disabled'
                                                              })
                                   )                            
    tipo = forms.ChoiceField(choices = TIPO_ESTADO, required=True, label="Tipo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true',
                                                              'disabled':'disabled',  
                                                              })
                                   )
    fecha_ingreso_estimada = forms.CharField(required=True, label="Fecha Estimada Ingreso",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_examen", }))
    obs = forms.CharField (required=False, label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control",
                                                              'disabled':'disabled'}))
    planta = forms.ModelChoiceField(queryset=Planta.objects.filter(status=True), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true',
                                                              'disabled':'disabled'
                                                              })
                                   )
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.filter(status=True), required=True, label="Cargo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true',
                                                              'disabled':'disabled'
                                                              })
                                   )
    
    bateria = forms.ModelChoiceField(queryset=Bateria.objects.filter(status=True), required=False, label="Batería",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true',
                                                              'disabled':'disabled',
                                                              })
                                   )
    requerimiento = forms.ModelChoiceField(queryset=Requerimiento.objects.filter(status=True), required=True, label="Requerimiento",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true',
                                                              'disabled':'disabled',                                                            
                                                              })
                                   )
    hal2 =forms.BooleanField(required=False, label='Hal2',
                                 widget=forms.CheckboxInput(attrs={'class': "form-control-lg",
                                                              'disabled':'disabled',}))
    referido =forms.BooleanField(required=False, label='Referido',
                                 widget=forms.CheckboxInput(attrs={'class': "form-control-lg",
                                                              'disabled':'disabled',}))
          
    class Meta:
        model = Agendamiento
        fields = ("trabajador", "tipo", "referido", "hal2", "fecha_ingreso_estimada", "fecha_agenda_evaluacion", "obs", "planta", "cargo", "bateria", "requerimiento")

    