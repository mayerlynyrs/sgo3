"""Examenes Forms"""

# Django
from django import forms
from sgo.utils.models import Planta
# sgo Model
from utils.models import Cliente
from requerimientos.models import Requerimiento


class RequerimientoCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control-lg"}))
    comentario = forms.CharField(required=True, label="Comentario",
                                widget=forms.Textarea(attrs={'class': "form-control-lg"}))

    # clientes = forms.ModelMultipleChoiceField(queryset=Cliente.objects.none(), required=True, label="Cliente",
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
            self.fields['plantas'].queryset = Planta.objects.filter(id__in=user.planta.all())
        else:
            self.fields['plantas'].queryset = Planta.objects.all()

    class Meta:
        model = Requerimiento
        fields = ("nombre", "centro_costo", "comentario", "planta", "status", )
