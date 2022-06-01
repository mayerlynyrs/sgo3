"""Examenes Forms"""

# Django
from django import forms
# sgo Model
from clientes.models import Cliente
from examenes.models import Examen, Bateria, CentroMedico
from agendamientos.models import Agendamiento
from clientes.models import Planta
from utils.models import Cargo, Region, Ciudad, Provincia




class ExamenForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    valor = forms.IntegerField(required=True, label="Valor",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(ExamenForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Examen
        fields = ("nombre", "valor")


class BateriaForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    examen = forms.ModelMultipleChoiceField(queryset=Examen.objects.all(), required=True, label="Exámenes",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick form-control',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                        })
                                            )

    def __init__(self, *args, **kwargs):
        super(BateriaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bateria
        fields = ('nombre', 'examen', )


class CentroForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    direccion = forms.CharField(required=True, label="Dirección",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True, label="Región",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(), required=True, label="Provincia",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.all(), required=True, label="Ciudad",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    class Meta:
        model = CentroMedico
        fields = ('nombre', 'direccion', 'region', 'provincia', 'ciudad', )


class AgendaGeneralForm(forms.ModelForm):

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
    centromedico = forms.ModelChoiceField(queryset=CentroMedico.objects.filter(status=True), required=True, label="Centro Medico",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )   


    class Meta:
        model = Agendamiento
        fields = ( "tipo", "referido", "hal2", "fecha_ingreso_estimada", "fecha_agenda_evaluacion", "obs", "planta", "estado", "cargo", "centro")

