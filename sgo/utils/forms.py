"""Utils Forms"""

# Django
from django import forms

# sgo Model
from utils.models import Area, Cargo, Horario, Bono
from users.models import Salud, Afp, ValoresDiario, ValoresDiarioAfp


class AreaForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AreaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Area
        fields = ("nombre",)


class CargoForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    alias = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    cod_uny_cargo = forms.CharField(required=True, label="Codigo Unysoft",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    descripcion = forms.CharField (required=True, label="Descripción",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cargo
        fields = ("nombre", "alias", "cod_uny_cargo", "descripcion")


class HorarioForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    descripcion = forms.CharField (required=True, label="Descripción",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(HorarioForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Horario
        fields = ("nombre","descripcion",)


class BonoForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    alias = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    descripcion = forms.CharField (required=True, label="Descripción", max_length=500,
                                 widget=forms.Textarea(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(BonoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bono
        fields = ("nombre", "alias", "descripcion",)


class SaludForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
                                 
    cod_uny_salud = forms.CharField(required=True, label="Código Unysoft",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(SaludForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Salud
        fields = ("nombre", "cod_uny_salud",)


class AfpForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    cod_uny_afp = forms.CharField(required=True, label="Código AFP",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    tasa = forms.FloatField(required=True, label="Tasa",
                                 widget=forms.NumberInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))

    def __init__(self, *args, **kwargs):
        super(AfpForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Afp
        fields = ("nombre","cod_uny_afp", "tasa",)


class ValoresDiarioForm(forms.ModelForm):
    valor_diario = forms.CharField(required=True, label="Valor Diario",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))

    def __init__(self, *args, **kwargs):
        super(ValoresDiarioForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ValoresDiario
        fields = ("valor_diario",)


class ValoresDiarioAfpForm(forms.ModelForm):
    valor = forms.CharField(required=True, label="Valor",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))
    afp = forms.ModelChoiceField(queryset=Afp.objects.all(), required=True, label="Afp",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    valor_diario = forms.ModelChoiceField(queryset=ValoresDiario.objects.all(), required=True, label="Valores Diarios",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    def __init__(self, *args, **kwargs):
        super(ValoresDiarioAfpForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ValoresDiarioAfp
        fields = ("valor", "afp", "valor_diario",)
