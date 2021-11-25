"""Requerimiento Forms"""

# Django
from django import forms
# sgo Model
from utils.models import Planta
from requerimientos.models import Requerimiento, Causal


class RequerimientoCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control-lg"}))

    # plantas = forms.ModelMultipleChoiceField(queryset=Planta.objects.none(), required=True, label="Planta",
    #                                         widget=forms.SelectMultiple(
    #                                             attrs={'class': 'selectpicker show-tick',
    #                                                    'data-size': '5',
    #                                                    'data-live-search': 'true',
    #                                                    'data-live-search-normalize': 'true'
    #                                                    })
    #                                         )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(RequerimientoCreateForm, self).__init__(*args, **kwargs)
        if not user.groups.filter(name='Administrador').exists():
            self.fields['planta'].queryset = Planta.objects.filter(id__in=user.planta.all())
            self.fields['causal'].queryset = Causal.objects.filter(id__in=user.causal.all())
        else:
            self.fields['planta'].queryset = Planta.objects.all()
            self.fields['causal'].queryset = Causal.objects.all()

    class Meta:
        model = Requerimiento
        fields = ("codigo", "centro_costo", "nombre", "fecha_solicitud", "regimen", "fecha_inicio", "fecha_termino",
                  "descripcion", "planta", "causal", "status", )
