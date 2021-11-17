"""Fichero Forms"""

# Django
from django import forms
from django.contrib.auth.models import Group
# sgo Model
from utils.models import Cliente, Negocio
from ficheros.models import Fichero


class FicheroCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control-lg"}))
    desc = forms.CharField(required=True, label="Descripción",
                                widget=forms.Textarea(attrs={'class': "form-control-lg"}))

    clientes = forms.ModelMultipleChoiceField(queryset=Cliente.objects.none(), required=True, label="Cliente",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )
    negocios = forms.ModelMultipleChoiceField(queryset=Negocio.objects.none(), required=True, label="Negocio",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(FicheroCreateForm, self).__init__(*args, **kwargs)
        if not user.groups.filter(name='Administrador').exists():
            self.fields['clientes'].queryset = Cliente.objects.filter(id__in=user.cliente.all())
            self.fields['negocios'].queryset = Negocio.objects.filter(id__in=user.negocio.all())
        else:
            self.fields['clientes'].queryset = Cliente.objects.all()
            self.fields['negocios'].queryset = Negocio.objects.all()

    class Meta:
        model = Fichero
        fields = ("nombre", "desc", "url", "clientes", "negocios", "status", )

