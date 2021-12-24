"""Users Forms"""

# Django
from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput

# sgo Model
from utils.models import Area, Cargo , Horario

User = get_user_model()


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
    descripcion = forms.CharField (required=True, label="Descripcion",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cargo
        fields = ("nombre","descripcion",)

class HorarioForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    descripcion = forms.CharField (required=True, label="Descripcion",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(HorarioForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Horario
        fields = ("nombre","descripcion",)