"""Epps Forms"""

# Django
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

# sgo Model
from clientes.models import Cliente, Planta
from epps.models import TipoInsumo, Insumo, Convenio, ConvenioRequerimiento
#Requerimientos
from requerimientos.models import AreaCargo


class TipoInsumoForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(TipoInsumoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TipoInsumo
        fields = ("nombre",)


class InsumoForm(forms.ModelForm):
    codigo_externo = forms.CharField(required=True, label="Código Externo",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    costo = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))
    tipo_insumo = forms.ModelChoiceField(queryset=TipoInsumo.objects.filter(status=True), required=False, label="Tipo Insumo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    def __init__(self, *args, **kwargs):
        super(InsumoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Insumo
        fields = ("codigo_externo", "nombre", "costo", "tipo_insumo")


class ConvenioForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    valor = forms.CharField(required=True, label="Valor",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))
    validez = forms.CharField(required=True, label="Validez",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))
    insumo = forms.ModelMultipleChoiceField(queryset=Insumo.objects.all(), required=True, label="Insumos",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick form-control',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                        })
                                   )
    # cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(status=True), required=False, label="Cliente",
    #                                widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
    #                                                           'data-size': '5',
    #                                                           'data-live-search': 'true',
    #                                                           'data-live-search-normalize': 'true'
    #                                                           })
    #                                )
    # planta = forms.ModelChoiceField(queryset=Planta.objects.filter(status=True), required=False, label="Planta",
    #                                widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
    #                                                           'data-size': '5',
    #                                                           'data-live-search': 'true',
    #                                                           'data-live-search-normalize': 'true'
    #                                                           })
    #                                )
    created_date = forms.DateField(required=True, label="Fecha del Convenio",
                                widget=forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA','class': "form-control", 'autocomplete':'off', 'id':"fecha"}))

    def __init__(self, *args, **kwargs):
        super(ConvenioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('nombre', css_class='form-group col-md-6 mb-0'),
                Column('valor', css_class='form-group col-md-6 mb-0'),
                css_class='form-row col-md-12'
            ),
            Row(
                Column('validez', css_class='form-group col-md-6 mb-0'),
                Column('insumo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row col-md-12'
            ),
            # Row(
            #     Column('cliente', css_class='form-group col-md-6 mb-0'),
            #     Column('planta', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row col-md-12'
            # ),       

        )


    class Meta:
        model = Convenio
        fields = ("nombre", "valor", "validez", "insumo")


class ConvenioRequerForm(forms.ModelForm):
    convenio = forms.ModelChoiceField(queryset=Convenio.objects.none(), required=True,
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    area_cargo = forms.ModelChoiceField(queryset=AreaCargo.objects.none(), required=True, label="Área Cargo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )


    def __init__(self, *args, **kwargs):
        convenio = kwargs.pop('convenio', None)
        area_cargo = kwargs.pop('area_cargo', None)
        super(ConvenioRequerForm, self).__init__(*args, **kwargs)
        
        self.fields['convenio'].queryset = convenio
        self.fields['area_cargo'].queryset = area_cargo

    class Meta:
        model = ConvenioRequerimiento
        fields = ("convenio", "area_cargo")
