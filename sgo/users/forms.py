"""Users Forms"""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from datetime import datetime

from django.forms import *
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django.forms import inlineformset_factory, RadioSelect
from django.contrib.auth import get_user_model
from django.forms import TextInput
# sgo Model
from clientes.models import Cliente, Negocio, Planta
from utils.models import Region, Provincia, Ciudad
from examenes.models import Evaluacion , Examen
from users.models import Trabajador, Civil, Salud, Afp, Profesion, ProfesionTrabajador, Especialidad, NivelEstudio, TipoCta, Parentesco, Contacto, TipoArchivo, ArchivoTrabajador, ListaNegra, Banco , Nacionalidad, Ciudad

User = get_user_model()


class ProfesionForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfesionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profesion
        fields = ("nombre", )

class EspecialidadForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
  

    def __init__(self, *args, **kwargs):
        super(EspecialidadForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Especialidad
        fields = ("nombre", )


class ParentescoCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(ParentescoCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Parentesco
        fields = ("nombre", "status", )


class TipoArchivoCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(TipoArchivoCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TipoArchivo
        fields = ("nombre", "status", )


class CrearUsuarioForm(forms.ModelForm):
    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'onblur': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': 'Ingrese RUT sin puntos ni guión',})
                          )
    
    first_name = forms.CharField(required=True, label="Nombres",
                                 widget=forms.TextInput(attrs={'class': "form-control" }))
    last_name = forms.CharField(required=True, label="Apellidos",
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': "form-control"}))
    fecha_nacimiento = forms.DateField(required=True, label="Fecha de Nacimiento",
                                widget=forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA','class': "form-control", 'autocomplete':'off', 'id':"fecha"}))
    group = forms.ModelChoiceField(queryset=Group.objects.none(), required=True, label="Perfil",
                                   widget=forms.Select(attrs={'class': 'selectpicker form-control ',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cliente = forms.ModelMultipleChoiceField(queryset=Cliente.objects.filter(status=True), required=True, label="Cliente",
                                            widget=forms.SelectMultiple(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    # negocio = forms.ModelMultipleChoiceField(queryset=Negocio.objects.filter(status=True), required=True, label="Negocio",
    #                                         widget=forms.SelectMultiple(
    #                                             attrs={'class': 'selectpicker show-tick',
    #                                                    'data-size': '5',
    #                                                    'data-live-search': 'true',
    #                                                    'data-live-search-normalize': 'true'
    #                                                    })
    #                                         )
    planta = forms.ModelMultipleChoiceField(queryset=Planta.objects.filter(status=True), required=True, label="Plantas",
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
        super(CrearUsuarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('group', css_class='form-group col-md-6 mb-0'),
                Column('rut', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fecha_nacimiento', css_class='form-group col-md-6 mb-0'),
                Column('telefono', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-0'),
                Column('planta', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            # 'check_me_out',
            # Submit('submit', 'Sign in')
        )
        if not user.groups.filter(name='Administrador').exists():
            self.fields['group'].queryset = Group.objects.exclude(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT', ])
            self.fields['cliente'].queryset = Cliente.objects.filter(id__in=user.cliente.all())
            # self.fields['negocio'].queryset = Negocio.objects.filter(id__in=user.negocio.all())
            self.fields['planta'].queryset = Planta.objects.filter(id__in=user.planta.all())
            cliente_id = self.data.get('cliente')
            # self.fields['negocio'].queryset = negocio.objects.filter(cliente_id=cliente_id).order_by('nombre')
        else:
            self.fields['group'].queryset = Group.objects.exclude(name__in=['Trabajador', ])
            self.fields['cliente'].queryset = Cliente.objects.all()
            # self.fields['negocio'].queryset = Negocio.objects.all()
            self.fields['planta'].queryset = Planta.objects.all()


    class Meta:
        model = User
        fields = ("group", "rut", "first_name", "last_name", "email", "telefono", "fecha_nacimiento", "cliente", "planta", "is_active", )
        exclude = ('password1', 'password2')
        widgets = {
            'telefono': TextInput(attrs={
                'class': "form-control",
                'type': "number",
                'placeholder': '56912345678',
                }),
        }


class EditarUsuarioForm(forms.ModelForm):
    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'onblur': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': 'Ingrese RUT sin puntos ni guión',})
                          )
    first_name = forms.CharField(required=True, label="Nombres",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(required=True, label="Apellidos",
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': "form-control"}))
    
    fecha_nacimiento = forms.DateField(required=True, label="Fecha de Nacimiento",
                                widget=forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA','class': "form-control", 'autocomplete':'off', 'id':"fecha"}))
    group = forms.ModelChoiceField(queryset=Group.objects.none(), required=True, label="Perfil",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cliente = forms.ModelMultipleChoiceField(queryset=Cliente.objects.filter(status=True), required=True, label="Cliente",
                                   widget=forms.SelectMultiple(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    planta = forms.ModelMultipleChoiceField(queryset=Planta.objects.filter(status=True), required=True, label="Plantas",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )

        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print('edit')
        print(user)
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('group', css_class='form-group col-md-6 mb-0'),
                Column('rut', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fecha_nacimiento', css_class='form-group col-md-6 mb-0'),
                Column('telefono', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-0'),
                Column('planta', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

        # if not user.groups.filter(name='Administrador').exists():
        if not user.groups.filter(name='Administrador').exists():
            self.fields['group'].queryset = Group.objects.exclude(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT', ])
            self.fields['cliente'].queryset = Cliente.objects.filter(id__in=user.cliente.all())
            self.fields['planta'].queryset = Planta.objects.filter(id__in=user.planta.all())
        else:
            self.fields['group'].queryset = Group.objects.exclude(name__in=['Trabajador', ])
            self.fields['cliente'].queryset = Cliente.objects.all()
            self.fields['planta'].queryset = Planta.objects.all()

 
    class Meta:
        model = User
        fields = ("group", "rut", "first_name", "last_name", "email", "telefono", "fecha_nacimiento", "cliente", "planta", "is_active", )
        widgets = {
            'telefono': TextInput(attrs={
                'class': "form-control",
                'type': "number",
                'placeholder': '56912345678'
                }),
            'fecha_nacimiento': TextInput(attrs={
                'placeholder': 'DD/MM/AAAA',
                'class': "form-control",
                'type':"date",
                'id':"start"
                }),
        }


class CrearTrabajadorForm(forms.ModelForm):
    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'onblur': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': 'Ingrese RUT sin puntos ni guión',})
                          )
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': "form-control"}))
    
    first_name = forms.CharField(required=True, label="Nombres",
                                 widget=forms.TextInput(attrs={'class': "form-control" }))
    last_name = forms.CharField(required=True, label="Apellidos",
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    telefono2 = forms.CharField(required=True, label="Teléfono",
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    fecha_nacimiento = forms.DateField(required=True, label="Fecha de Nacimiento",
                                widget=forms.TextInput(attrs={'placeholder': 'DD-MM-AAAA','class': "form-control", 'autocomplete':'off' ,'id':"fecha"}))
    estado_civil = forms.ModelChoiceField(queryset=Civil.objects.filter(status=True), required=True, label="Estado Civil",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    salud = forms.ModelChoiceField(queryset=Salud.objects.filter(status=True), required=True, label="Sistema Salud",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    nacionalidad = forms.ModelChoiceField(queryset=Nacionalidad.objects.filter(status=True), required=True, label="Nacionalidad",
                                            widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.filter(status=True), required=True, label="Ciudad",
                                            widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    pacto_uf = forms.CharField(required=True, label="Pacto UF",
                                widget=forms.TextInput(attrs={'class': "form-control", 'type': 'number'}))
    afp = forms.ModelChoiceField(queryset=Afp.objects.filter(status=True), required=True, label="Sistema Prevision",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.filter(status=True), required=True, label="Especialidad",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    nivel_estudio = forms.ModelChoiceField(queryset=NivelEstudio.objects.filter(status=True), required=True, label="Nivel de Estudio",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    tipo_cuenta = forms.ModelChoiceField(queryset=TipoCta.objects.filter(status=True), required=True, label="Tipo Cuenta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cuenta = forms.CharField(required=True, label="Número de Cuenta",
                                widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))

    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(status=True), required=True, label="Cliente",
                                            widget=forms.Select(
                                                attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    banco = forms.ModelChoiceField(queryset=Banco.objects.filter(status=True), required=True, label="Banco",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    # negocio = forms.ModelMultipleChoiceField(queryset=Negocio.objects.filter(status=True), required=True, label="Negocio",
    #                                         widget=forms.SelectMultiple(
    #                                             attrs={'class': 'selectpicker show-tick',
    #                                                    'data-size': '5',
    #                                                    'data-live-search': 'true',
    #                                                    'data-live-search-normalize': 'true'
    #                                                    })
    #                                         )
    planta = forms.ModelChoiceField(queryset=Planta.objects.filter(status=True), required=True, label="Plantas",
                                            widget=forms.Select(
                                                attrs={'class': 'show-tick form-control',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )
    calzado = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))
    

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(CrearTrabajadorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('rut', css_class='form-group col-md-6 mb-0'),
                Column('pasaporte', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fecha_nacimiento', css_class='form-group col-md-6 mb-0'),
                Column('sexo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                # Column('telefono', css_class='form-group col-md-6 mb-0'),
                Column('telefono2', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('estado_civil', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nacionalidad', css_class='form-group col-md-6 mb-0'),
                Column('foto', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('region', css_class='form-group col-md-4 mb-0'),
                Column('provincia', css_class='form-group col-md-4 mb-0'),
                Column('ciudad', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'domicilio',
            Row(
                Column('afp', css_class='form-group col-md-4 mb-0'),
                Column('salud', css_class='form-group col-md-4 mb-0'),
                Column('pacto_uf', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('especialidad', css_class='form-group col-md-6 mb-0'),
                Column('nivel_estudio', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('banco', css_class='form-group col-md-4 mb-0'),
                Column('tipo_cuenta', css_class='form-group col-md-4 mb-0'),
                Column('cuenta', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('talla_polera', css_class='form-group col-md-4 mb-0'),
                Column('talla_pantalon', css_class='form-group col-md-4 mb-0'),
                Column('calzado', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('licencia_conducir', css_class='form-group col-md-6 mb-0'),
                Column('examen', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-0'),
                Column('planta', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            # 'check_me_out',
            # Submit('submit', 'Sign in')
        )
        if not user.groups.filter(name='Administrador').exists():
            # self.fields['group'].queryset = Group.objects.exclude(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT', ])
            self.fields['cliente'].queryset = Cliente.objects.filter(id__in=user.cliente.all())
            # self.fields['negocio'].queryset = Negocio.objects.filter(id__in=user.negocio.all())
            self.fields['planta'].queryset = Planta.objects.filter(id__in=user.planta.all())
            cliente_id = self.data.get('cliente')
            # self.fields['negocio'].queryset = negocio.objects.filter(cliente_id=cliente_id).order_by('nombre')
        else:
            # self.fields['group'].queryset = Group.objects.all()
            self.fields['cliente'].queryset = Cliente.objects.all()
            # self.fields['negocio'].queryset = Negocio.objects.all()
            self.fields['planta'].queryset = Planta.objects.all()


    class Meta:
        model = Trabajador
        fields = ("rut", "pasaporte", "first_name", "last_name", "sexo", "email", "telefono2",
                  "estado_civil", "fecha_nacimiento", "nacionalidad", "licencia_conducir", "talla_polera", "talla_pantalon", "calzado",
                  "nivel_estudio", "especialidad", "region", "provincia", "ciudad", "domicilio", "afp", "salud", "pacto_uf", "examen",
                   "foto", "banco", "tipo_cuenta", "cuenta", "cliente", "planta", "is_active", )
        exclude = ('password1', 'password2')
        widgets = {
            'telefono2': TextInput(attrs={
                'class': "form-control",
                'type': "number",
                'placeholder': '56912345678',
                }),
            'cuenta': TextInput(attrs={
                'class': "form-control",
                'type': "number"
                }),
        }


class EditarTrabajadorForm(forms.ModelForm):
    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'onblur': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': 'Ingrese RUT sin puntos ni guión',})
                          )
    first_name = forms.CharField(required=True, label="Nombres",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(required=True, label="Apellidos",
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': "form-control"}))
    domicilio = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': "form-control"}))
    
    fecha_nacimiento = forms.DateField(required=True, label="Fecha de Nacimiento",
                                widget=forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA','class': "form-control", 'autocomplete':'off', 'id':"fecha"}))
    estado_civil = forms.ModelChoiceField(queryset=Civil.objects.filter(status=True), required=True, label="Estado Civil",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    salud = forms.ModelChoiceField(queryset=Salud.objects.filter(status=True), required=True, label="Sistema Salud",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    pacto_uf = forms.CharField(required=True, label="Pacto UF",
                                widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))
    afp = forms.ModelChoiceField(queryset=Afp.objects.filter(status=True), required=True, label="Sistema Prevision",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    tipo_cuenta = forms.ModelChoiceField(queryset=TipoCta.objects.filter(status=True), required=True, label="Tipo Cuenta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cuenta = forms.CharField(required=True, label="Número de Cuenta",
                                widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))
    calzado = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))

        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print('editar trabajador user')
        print(user)
        trabajador = kwargs.pop('trabajador', None)
        print('editar trabajador')
        print(trabajador)
        super(EditarTrabajadorForm, self).__init__(*args, **kwargs)

        self.fields['provincia'].queryset = Provincia.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['provincia'].queryset = Provincia.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Provincia queryset
        elif self.instance.pk:
            self.fields['provincia'].queryset = self.instance.region.provincia_set.order_by('nombre')

        self.fields['ciudad'].queryset = Provincia.objects.none()

        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Provincia queryset
        elif self.instance.pk:
            # self.fields['ciudad'].queryset = self.instance.region.provincia.ciudad_set.order_by('nombre')
            self.fields['ciudad'].queryset = self.instance.provincia.ciudad_set.order_by('nombre')

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('rut', css_class='form-group col-md-6 mb-0'),
                Column('pasaporte', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fecha_nacimiento', css_class='form-group col-md-6 mb-0'),
                Column('sexo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6 mb-0'),
                Column('telefono2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('estado_civil', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nacionalidad', css_class='form-group col-md-6 mb-0'),
                Column('foto', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('region', css_class='form-group col-md-4 mb-0'),
                Column('provincia', css_class='form-group col-md-4 mb-0'),
                Column('ciudad', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'domicilio',
            Row(
                Column('afp', css_class='form-group col-md-4 mb-0'),
                Column('salud', css_class='form-group col-md-4 mb-0'),
                Column('pacto_uf', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('especialidad', css_class='form-group col-md-6 mb-0'),
                Column('nivel_estudio', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('banco', css_class='form-group col-md-4 mb-0'),
                Column('tipo_cuenta', css_class='form-group col-md-4 mb-0'),
                Column('cuenta', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('talla_polera', css_class='form-group col-md-4 mb-0'),
                Column('talla_pantalon', css_class='form-group col-md-4 mb-0'),
                Column('calzado', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('licencia_conducir', css_class='form-group col-md-6 mb-0'),
                Column('examen', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

        )


 
    class Meta:
        model = Trabajador
        fields = ( "rut", "pasaporte", "first_name", "last_name", "sexo", "email", "telefono", "telefono2",
                  "estado_civil", "fecha_nacimiento", "nacionalidad", "licencia_conducir", "talla_polera", "talla_pantalon", "calzado",
                  "nivel_estudio", "especialidad", "region", "provincia", "ciudad", "domicilio", "afp", "salud", "pacto_uf", "examen", 
                   "foto", "banco", "tipo_cuenta", "cuenta", "is_active", )
        widgets = {
            'telefono': TextInput(attrs={
                'class': "form-control",
                'type': "number",
                'placeholder': '56912345678'
                }),
            'cuenta': TextInput(attrs={
                'class': "form-control",
                'type': "number"
                }),
            'fecha_nacimiento': TextInput(attrs={
                'placeholder': 'DD/MM/AAAA',
                'class': "form-control",
                'type':"date",
                'id':"start"
                }),
        }


class ListaNegraForm(forms.ModelForm):
    LISTA_NEGRA = 'LN'
    LISTA_NEGRA_PLANTA = 'LNP'

    TIPO_LN = (
        (LISTA_NEGRA, 'Lista Negra'),
        (LISTA_NEGRA_PLANTA, 'Lista Negra por Planta'),
    )

    tipo = forms.ChoiceField(choices = TIPO_LN, required=True,
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    descripcion = forms.CharField (required=True, label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))
    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.filter(is_active=True), required=True,
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    planta = forms.ModelChoiceField(queryset=Planta.objects.filter(status=True), required=False, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    def __init__(self, *args, **kwargs):
        trabajador = kwargs.pop('trabajador', None)
        super(ListaNegraForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ListaNegra
        fields = ("tipo", "descripcion", "trabajador", "planta", )


class ProfesionTrabajadorForm(forms.ModelForm):
    egreso = forms.CharField(required=True, label="Egreso",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off',  'id':"egreso"}))
    institucion = forms.CharField(required=True, label="Institución",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    profesion = forms.ModelChoiceField(queryset=Profesion.objects.filter(status=True), required=True, label="Profesión",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfesionTrabajadorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ProfesionTrabajador
        fields = ("egreso", "institucion", "profesion", )


class ContactoForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    telefono = forms.CharField(required=True, label="Teléfono",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    parentesco = forms.ModelChoiceField(queryset=Parentesco.objects.filter(status=True), required=True, label="Parentesco",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContactoForm, self).__init__(*args, **kwargs)

    # validamos el campo "materia"
    def clean_materia(self):
        # Obtenermos los datos del form
        parentesco = self.cleaned_data.get('parentesco')

        # Si existe una instancia con el mismo docente y materia entramos al if
        if Contacto.objects.filter(nombre='marina', parentesco_id = parentesco.id, user_id=2).exists():
            print('se repite')
            # Mandamos un error al form con un mensaje
            raise forms.ValidationError('No se puede asignar la misma materia a un docente 2 veses')

    class Meta:
        model = Contacto
        fields = ("nombre", "telefono", "parentesco", )


class ArchivoTrabajadorForm(forms.ModelForm):
    tipo_archivo = forms.ModelChoiceField(queryset=TipoArchivo.objects.filter(status=True), required=True, label="Tipo Archivo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ArchivoTrabajadorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ArchivoTrabajador
        fields = ("tipo_archivo", "archivo", )


class EditarAtributosForm(forms.ModelForm):
    atributos = forms.JSONField(required=True, label="Más Información",
                                widget=forms.Textarea(attrs={'class': "form-control",
                                                             'placeholder': '{"cargo": 23, "departamento": 17, "jornada": "Diurna", "sueldo": "500.000", "beneficio": "Si", "fecha_ingreso": "12/10/2021", "hora_ingreso": "08:30", "fecha_termino": "10/01/2022"}',}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(EditarAtributosForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("atributos", )
        exclude = ('group', 'rut', 'first_name', 'last_name', 'sexo', 'email', 'telefono', 'estado_civil', 'fecha_nacimiento', 
                  'nacionalidad', 'region', 'provincia', 'ciudad', 'domicilio', 'salud', 'afp',
                  'banco', 'tipo_cuenta', 'cuenta', 'cliente', 'negocio', 'is_active', 'password1', 'password2')


class EvaluacionAchivoForm(forms.ModelForm):

    APROBADO = 'A'
    RECHAZADO = 'R'
    EVALUADO = 'E'

    RESULTADOS_ESTADO = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (EVALUADO, 'Evaluado'),
    )

    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    fecha_examen = forms.CharField(required=True, label="Fecha Examen",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_examen", }))
    fecha_vigencia = forms.CharField(required=True, label="Fecha Vigencia",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_vigencia"}))
    descripcion = forms.CharField (required=True, label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))
    valor_examen = forms.CharField(required=True, label="Valor Examen",
                                widget=forms.TextInput(attrs={'class': "form-control"}))                              
    resultado = forms.ChoiceField(choices = RESULTADOS_ESTADO, required=True, label="Resultado",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    examen = forms.ModelChoiceField(queryset=Examen.objects.all(), required=True, label="Tipo Examen",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    archivo = forms.FileField()
    planta = forms.ModelChoiceField(queryset=Planta.objects.filter(status=True), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EvaluacionAchivoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Evaluacion
        fields = ("nombre", "fecha_examen", "fecha_vigencia", "descripcion", "valor_examen", "resultado", "referido", "archivo", "examen" )
