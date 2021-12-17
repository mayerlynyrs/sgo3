"""Users Forms"""

# Django
from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput

# sgo Model
from utils.models import Area, Cargo , Horario

User = get_user_model()


class AreaCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AreaCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Area
        fields = ("nombre", "status", )

class CargoCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(CargoCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cargo
        fields = ("nombre","descripcion", "status", )

class HorarioCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(HorarioCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Horario
        fields = ("nombre","descripcion", "status", )