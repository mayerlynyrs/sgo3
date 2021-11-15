"""Contratos Forms."""

# Django
from django import forms
# Model
from contratos.models import Plantilla
from utils.models import Cliente, Planta


class CrearPlantillaForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                             widget=forms.TextInput(attrs={'class': "form-control-lg"}))
    clientes = forms.ModelMultipleChoiceField(queryset=Cliente.objects.all(), required=True, label="Cliente",
                                   widget=forms.SelectMultiple(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    plantas = forms.ModelMultipleChoiceField(queryset=Planta.objects.all(), required=True, label="Planta",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CrearPlantillaForm, self).__init__(*args, **kwargs)
        if not user.groups.filter(name='Administrador').exists():
            self.fields['clientes'].queryset = Cliente.objects.filter(id__in=user.cliente.all())
            self.fields['plantas'].queryset = Planta.objects.filter(id__in=user.planta.all())
        else:
            self.fields['clientes'].queryset = Cliente.objects.all()
            self.fields['plantas'].queryset = Planta.objects.all()


    class Meta:
        model = Plantilla
        fields = ("nombre", "tipo", "archivo",  "clientes", "plantas", )


class ActualizarPlantillaForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                             widget=forms.TextInput(attrs={'class': "form-control-lg"}))

    clientes = forms.ModelMultipleChoiceField(queryset=Cliente.objects.none(), required=True, label="Cliente",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )
    plantas = forms.ModelMultipleChoiceField(queryset=Planta.objects.none(), required=True, label="Planta",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ActualizarPlantillaForm, self).__init__(*args, **kwargs)
        if not user.groups.filter(name='Administrador').exists():
            self.fields['clientes'].queryset = Cliente.objects.filter(id__in=user.cliente.all())
            self.fields['plantas'].queryset = Planta.objects.filter(id__in=user.planta.all())
        else:
            self.fields['clientes'].queryset = Cliente.objects.all()
            self.fields['plantas'].queryset = Planta.objects.all()


    class Meta:
        model = Plantilla
        fields = ("nombre", "tipo", "archivo", "clientes", "plantas", 'activo')
