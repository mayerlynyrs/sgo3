"""Examenes Forms"""

# Django
from django import forms
# sgo Model
from utils.models import Cliente
from examenes.models import Examen, Bateria


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
                                            widget=forms.SelectMultiple(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    def __init__(self, *args, **kwargs):
        super(BateriaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bateria
        fields = ("nombre", "examen")
