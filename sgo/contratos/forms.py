"""Contratos Forms."""

# Django
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
# Model
from contratos.models import Plantilla, TipoContrato, Contrato
from clientes.models import Cliente, Planta


class TipoContratoForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
  

    def __init__(self, *args, **kwargs):
        super(TipoContratoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TipoContrato
        fields = ("nombre", )


class CrearContratoForm(forms.ModelForm):
    fecha_pago = forms.CharField(required=True, label="Fecha Pago",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_solicitud", 'readonly' :'true'}))
    fecha_inicio = forms.CharField(required=True, label="Fecha Inicio",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_inicio", 'readonly' :'true'}))
    fecha_termino = forms.CharField(required=True, label="Fecha Término",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_termino",'readonly' :'true' }))
    # nombre = forms.CharField(required=True, label="Nombre",
    #                          widget=forms.TextInput(attrs={'class': "form-control"}))
    clientes = forms.ModelMultipleChoiceField(queryset=Cliente.objects.all(), required=True, label="Cliente",
                                   widget=forms.SelectMultiple(attrs={'class': 'selectpicker show-tick form-control',
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
        super(CrearContratoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('tipo_contrato', css_class='form-group col-md-4 mb-0'),
                Column('sueldo_base', css_class='form-group col-md-4 mb-0'),
                Column('causal', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fecha_pago', css_class='form-group col-md-4 mb-0'),
                Column('fecha_inicio', css_class='form-group col-md-4 mb-0'),
                Column('fecha_termino', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('gratificacion', css_class='form-group col-md-4 mb-0'),
                Column('horario', css_class='form-group col-md-4 mb-0'),
                Column('planta', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'seguro_vida',
            'motivo',
        )
        # if not user.groups.filter(name='Administrador').exists():
        #     self.fields['clientes'].queryset = Cliente.objects.filter(id__in=user.cliente.all())
        #     self.fields['plantas'].queryset = Planta.objects.filter(id__in=user.planta.all())
        # else:
        #     self.fields['clientes'].queryset = Cliente.objects.all()
        #     self.fields['plantas'].queryset = Planta.objects.all()


    class Meta:
        model = Contrato
        fields = ("tipo_contrato", "sueldo_base", "fecha_pago", "fecha_inicio",  "fecha_termino", "motivo", "seguro_vida", "gratificacion", "horario", "planta", "causal", )


class CrearPlantillaForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                             widget=forms.TextInput(attrs={'class': "form-control"}))
    clientes = forms.ModelMultipleChoiceField(queryset=Cliente.objects.all(), required=True, label="Cliente",
                                   widget=forms.SelectMultiple(attrs={'class': 'selectpicker show-tick form-control',
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
                             widget=forms.TextInput(attrs={'class': "form-control"}))

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
