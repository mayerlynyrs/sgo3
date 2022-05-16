"""Requerimiento Forms"""

# Django
from dataclasses import fields
from tokenize import group
from django import forms
# sgo Model
from clientes.models import Planta , Cliente
from requerimientos.models import Requerimiento



class ConsultaClienteForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=True, label="Cliente",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    planta = forms.ModelChoiceField(queryset=Planta.objects.all(), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )


    class Meta:
        model = Requerimiento
        fields = ("planta","cliente", )