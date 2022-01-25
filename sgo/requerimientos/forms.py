"""Requerimiento Forms"""

# Django
from django import forms
# sgo Model
from utils.models import Planta
from requerimientos.models import Requerimiento, Causal
from utils.models import Planta


class RequerimientoCreateForm(forms.ModelForm):

    NORMAL = 'NOR'
    PARADA_GENERAL_PLANTA = 'PGP'
    URGENCIA = 'URG'

    REGIMEN_ESTADO = (
        (NORMAL, 'Normal'),
        (PARADA_GENERAL_PLANTA, 'Parada Planta'),
        (URGENCIA, 'Urgencia'),
    )

    codigo = forms.CharField(required=True, label="Codigo",
                             widget=forms.TextInput(attrs={'class': "form-control" }))
    centro_costo = forms.CharField(required=True, label="Centro de costo",
                             widget=forms.TextInput(attrs={'class': "form-control" }))
    nombre = forms.CharField(required=True, label="Nombre Solicitud",
                             widget=forms.TextInput(attrs={'class': "form-control" }))
    fecha_solicitud = forms.CharField(required=True, label="Fecha Solicitud",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_solicitud", }))                              
    regimen = forms.ChoiceField(choices = REGIMEN_ESTADO, required=True, label="Regimen",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    fecha_inicio = forms.CharField(required=True, label="Fecha Inicio",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_inicio", }))
    fecha_termino = forms.CharField(required=True, label="Fecha Termino",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_termino", }))
    descripcion = forms.CharField (required=True, label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))
    causal = forms.ModelChoiceField(queryset=Causal.objects.all(), required=True, label="Causales",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control','onchange': 'getval(this);' ,
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    planta = forms.ModelChoiceField(queryset=Planta.objects.all(), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    class Meta:
        model = Requerimiento
        fields = ("codigo", "centro_costo", "nombre", "fecha_solicitud", "regimen", "fecha_inicio", "fecha_termino",
                  "descripcion", "planta", "causal", )
