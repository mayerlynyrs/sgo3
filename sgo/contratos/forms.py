"""Contratos Forms."""

# Django
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django.forms import TextInput
# Model
from contratos.models import Plantilla, TipoContrato, Contrato, TipoDocumento, Baja, MotivoBaja
from clientes.models import Cliente, Planta
from requerimientos.models import Causal
from utils.models import Horario, PuestaDisposicion
from users.models import ValoresDiario

class PuestaDisposicionForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'readonly': True}))
    gratificacion = forms.IntegerField(required=True, label="Gratificación",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'maxlength': 10, 'min': 1, 'type': 'number'}))
    seguro_cesantia = forms.CharField(required=True, label="Seguro de Cesantía",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'maxlength': 10}))
    seguro_invalidez = forms.CharField(required=True, label="Seguro de Invalidez",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'maxlength': 10}))
    seguro_vida = forms.CharField(required=True, label="Seguro de Vida",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'maxlength': 10}))
    mutual = forms.FloatField(required=True, label="Mutual",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'maxlength': 10, 'min': 1, 'type': 'number'}))
  

    def __init__(self, *args, **kwargs):
        super(PuestaDisposicionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PuestaDisposicion
        fields = ("nombre", "gratificacion", "seguro_cesantia", "seguro_invalidez", "seguro_vida", "mutual")

        widgets = {
            'gratificacion': TextInput(attrs={
                'class': "form-control",
                'type': "number",
                'maxlength': 10
                }),
        }


class TipoContratoForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
  

    def __init__(self, *args, **kwargs):
        super(TipoContratoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TipoContrato
        fields = ("nombre", )


class MotivoBajaForm(forms.ModelForm):

    motivo = forms.ModelChoiceField(queryset=MotivoBaja.objects.all(), required=True, label="Motivo",
                                   widget=forms.Select(attrs={'class': ' show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    def __init__(self, *args, **kwargs):
        super(MotivoBajaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Baja
        fields = ("motivo",)


class CrearContratoForm(forms.ModelForm):
    fecha_pago = forms.CharField(required=True, label="Fecha Pago",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_solicitud", 'readonly' :'true'}))
    fecha_inicio = forms.CharField(required=True, label="Fecha Inicio",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_inicio", 'readonly' :'true'}))
    fecha_termino = forms.CharField(required=True, label="Fecha Término",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_termino",'readonly' :'true' }))
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
                Column('tipo_documento', css_class='form-group col-md-4 mb-0'),
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

    class Meta:
        model = Contrato
        fields = ("tipo_documento", "sueldo_base", "fecha_pago", "fecha_inicio",  "fecha_termino", "motivo", "seguro_vida", "gratificacion", "horario", "planta", "causal", )


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
        fields = ("nombre", "tipo", "abreviatura", "archivo",  "clientes", "plantas", )
        widgets = {
            'abreviatura': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'ABCD'
                }),
        }


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
        fields = ("nombre", "tipo", "abreviatura", "archivo", "clientes", "plantas", 'activo')
        widgets = {
            'abreviatura': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'ABCD'
                }),
        }


class ContratoForm(forms.ModelForm):

    NORMAL = 'NOR'
    REGIMEN_PGP = 'PGP'
    URGENCIA = 'URG'
    CONTINGENCIA = "CON"

    REGIMEN_ESTADO = (
        (NORMAL, 'Normal'),
        (REGIMEN_PGP, 'Régimen PGP'),
        (URGENCIA, 'Urgencia'),
        (CONTINGENCIA, 'Contingencia'),
    )
    causal = forms.ModelChoiceField(queryset=Causal.objects.all(), required=True, label="Causal",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control','onchange': 'getval(this);' ,
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    motivo = forms.CharField (required=True, label="Observaciones",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    fecha_inicio = forms.CharField(required=True, label="Fecha Inicio",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_inicio", 'readonly' :'true'}))
    fecha_termino = forms.CharField(required=False, label="Fecha Término",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_termino",'readonly' :'true' }))
    horario = forms.ModelChoiceField(queryset=Horario.objects.none(), required=True, label="Horario",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true' 
                                                              })
                                   )
    sueldo_base = forms.CharField(required=False, label="sueldo",
                             widget=forms.TextInput(attrs={'class': "form-control"}))
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.filter(status=True, nombre__startswith=("Contrat")).exclude(nombre__startswith=("Contrato Diario")), required=False, label="Tipo Contrato",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    regimen = forms.ChoiceField(choices = REGIMEN_ESTADO, required=True, label="Régimen",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    valores_diario = forms.ModelChoiceField(queryset=ValoresDiario.objects.all(), required=False, label="Valores Diario",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    def __init__(self, *args, **kwargs):
        horario = kwargs.pop('horario', None)
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.fields['horario'].queryset = horario


    class Meta:
        model = Contrato
        fields = ("causal", "motivo", "fecha_inicio", "fecha_termino", "horario", 'sueldo_base', 'valores_diario', 'tipo_documento', 'regimen')


class ContratoEditarForm(forms.ModelForm):

    NORMAL = 'NOR'
    REGIMEN_PGP = 'PGP'
    URGENCIA = 'URG'
    CONTINGENCIA = "CON"
    REGIMEN_ESTADO = (
        (NORMAL, 'Normal'),
        (REGIMEN_PGP, 'Régimen PGP'),
        (URGENCIA, 'Urgencia'),
        (CONTINGENCIA, 'Contingencia'),
    )
    causal = forms.ModelChoiceField(queryset=Causal.objects.filter(status=True), required=False, label="Causal",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    motivo = forms.CharField (required=True, label="Observaciones",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    fecha_inicio = forms.CharField(required=True, label="Fecha Inicio",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_inicio", 'readonly' :'true'}))
    fecha_termino = forms.CharField(required=True, label="Fecha Término",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_termino",'readonly' :'true' }))
    horario = forms.ModelChoiceField(queryset=Horario.objects.none(), required=True, label="Horario",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true' 
                                                              })
                                   )
    sueldo_base = forms.CharField(required=True, label="sueldo",
                             widget=forms.TextInput(attrs={'class': "form-control"}))
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.filter(status=True, nombre__startswith='C'),required=False, label="Tipo Contrato",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )                              
    regimen = forms.ChoiceField(choices = REGIMEN_ESTADO, required=True, label="Regimen",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    valores_diario = forms.ModelChoiceField(queryset=ValoresDiario.objects.all(), required=False, label="Valores Diario",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true' 
                                                              })
                                   )
    def __init__(self, *args, **kwargs):
        horario = kwargs.pop('horario', None)
        super(ContratoEditarForm, self).__init__(*args, **kwargs)
        self.fields['horario'].queryset = horario

    class Meta:
        model = Contrato
        fields = ("causal", "motivo", "fecha_inicio", "fecha_termino", "horario", 'sueldo_base', 'tipo_documento', 'regimen', 'valores_diario')


class CompletasForm(forms.ModelForm):

    ENERO = '01'
    FEBRERO = '02'
    MARZO = '03'
    ABRIL = "04"
    MAYO = "05"
    JUNIO = "06"
    JULIO = "07"
    AGOSTO = "08"
    SEPTIEMBRE = "09"
    OCTUBRE = "10"
    NOVIEMBRE = "11"
    DICIEMBRE = "12"

    MESES_ESTADO = (
        (ENERO, 'Enero'),
        (FEBRERO, 'Febrero'),
        (MARZO, 'Marzo'),
        (ABRIL, 'Abril'),
        (MAYO, 'Mayo'),
        (JUNIO, 'Junio'),
        (JULIO, 'Julio'),
        (AGOSTO, 'Agosto'),
        (SEPTIEMBRE, 'Septiembre'),
        (OCTUBRE, 'Octubre'),
        (NOVIEMBRE, 'Noviembre'),
        (DICIEMBRE, 'Diciembre'),
    )
    planta = forms.ModelChoiceField(queryset=Planta.objects.all().order_by('nombre'), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    mes = forms.ChoiceField(choices = MESES_ESTADO, required=True, label="Mes",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true',
                                                              'disabled':'disabled'
                                                              })
                                   )


    class Meta:
        model = Contrato
        fields = ("planta","mes", )
