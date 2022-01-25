"""Users Forms"""

# Django
from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

# sgo Model
from utils.models import Area, Cargo, Horario, Bono, Cliente, Negocio, Gratificacion, Planta, Region, Ciudad, Provincia
from examenes.models import Examen
from users.models import Salud, Afp, ValoresDiario, ValoresDiarioAfp

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
    alias = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    descripcion = forms.CharField (required=True, label="Descripcion",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cargo
        fields = ("nombre", "alias", "descripcion",)


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


class BonoForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    descripcion = forms.CharField (required=True, label="Descripcion", max_length=500,
                                 widget=forms.Textarea(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(BonoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bono
        fields = ("nombre", "descripcion",)


class CrearClienteForm(forms.ModelForm):

    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'oninput': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': '987654321',}))
    
    razon_social = forms.CharField(required=True, label="Razon Social",
                             widget=forms.TextInput(attrs={'class': "form-control" }))
    giro = forms.CharField(required=True, label="Giro",
                             widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': "form-control"}))
    
    horario = forms.ModelMultipleChoiceField(queryset=Horario.objects.all(), required=True, label="Horarios",
                                            widget=forms.SelectMultiple(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cargo = forms.ModelMultipleChoiceField(queryset=Cargo.objects.all(), required=True, label="Cargos",
                                            widget=forms.SelectMultiple(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    area = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=True, label="Areas",
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
        super(CrearClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('rut', css_class='form-group col-md-6 mb-0'),
                Column('razon_social', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('giro', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('abreviatura', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('region', css_class='form-group col-md-4 mb-0'),
                Column('provincia', css_class='form-group col-md-4 mb-0'),
                Column('ciudad', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('direccion', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('area', css_class='form-group col-md-6 mb-0'),
                Column('cargo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('horario', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),         

        )
        # if not user..
        # .filter(name='Administrador').exists():
        #     self.fields['area'].queryset = Area.objects.exclude(id__in=user.Area.all())
        #     self.fields['cargo'].queryset = Cargo.objects.filter(id__in=user.Cargo.all())
        #     self.fields['horario'].queryset = Horario.objects.filter(id__in=user.Horario.all())
        # else:
        #     self.fields['area'].queryset = Area.objects.all()
        #     self.fields['cargo'].queryset = Cargo.objects.all()
        #     self.fields['horario'].queryset = Horario.objects.all()


    class Meta:
        model = Cliente
        fields = ("rut", "razon_social", "giro", "abreviatura", "email", "telefono", "area", "cargo", "horario",
                  "direccion", "region", "provincia", "ciudad", )
        widgets = {
            'telefono': TextInput(attrs={
                'class': "form-control",
                'type': "number",
                'placeholder': '56912345678',
                }),
            'abreviatura': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'ABCD'
                }),
        }


class EditarClienteForm(forms.ModelForm):
    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control",
                                    'onkeypress': "return isNumber(event)",
                                    'oninput': "checkRut(this)",
                                    'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                                    'placeholder': '987654321',})
                        )    
    razon_social = forms.CharField(required=True, label="Razón Social",
                             widget=forms.TextInput(attrs={'class': "form-control" }))
    giro = forms.CharField(required=True, label="Giro",
                             widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required=True, label="Correo",
                             widget=forms.EmailInput(attrs={'class': "form-control"}))
    
    horario = forms.ModelMultipleChoiceField(queryset=Horario.objects.all(), required=True, label="Horarios",
                                            widget=forms.SelectMultiple(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cargo = forms.ModelMultipleChoiceField(queryset=Cargo.objects.all(), required=True, label="Cargos",
                                            widget=forms.SelectMultiple(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    area = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=True, label="Áreas",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )

        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditarClienteForm, self).__init__(*args, **kwargs)

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
                Column('razon_social', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('giro', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('abreviatura', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('region', css_class='form-group col-md-4 mb-0'),
                Column('provincia', css_class='form-group col-md-4 mb-0'),
                Column('ciudad', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('direccion', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('area', css_class='form-group col-md-6 mb-0'),
                Column('cargo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('horario', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )

        # if not user.groups.filter(name='Administrador').exists():
        #     self.fields['group'].queryset = Group.objects.exclude(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT', ])
        #     self.fields['cliente'].queryset = Cliente.objects.filter(id__in=user.negocio.all())
        #     self.fields['negocio'].queryset = Negocio.objects.filter(id__in=user.negocio.all())
        # else:
        #     self.fields['group'].queryset = Group.objects.all()
        #     self.fields['cliente'].queryset = Cliente.objects.all()
        #     self.fields['negocio'].queryset = Negocio.objects.all()

 
    class Meta:
        model = Cliente
        fields = ("rut", "razon_social", "giro", "abreviatura", "email", "telefono", "area", "cargo", "horario",
                  "direccion", "region", "provincia", "ciudad", )
        widgets = {
            'telefono': TextInput(attrs={
                'class': "form-control",
                'type': "number",
                'placeholder': '56912345678'
                }),
            'abreviatura': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'ABCD'
                }),
        }


class NegocioForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    descripcion = forms.CharField (required=True, label="Descripcion",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))
    archivo = forms.FileField()

    def __init__(self, *args, **kwargs):
        Negocio = kwargs.pop('negocio', None)
        super(NegocioForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Negocio
        fields = ("nombre", "descripcion", "archivo")

class PlantaForm(forms.ModelForm):
    negocio = forms.ModelChoiceField(queryset=Negocio.objects.all(), required=True, label="Negocio",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control ',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'oninput': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': '987654321',})
                          ) 
    nombre = forms.CharField(required=True, label="Razon social",
                                 widget=forms.TextInput(attrs={'class': "form-control "}))
    direccion = forms.CharField (required=True, label="direccion",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    rut_gerente = forms.CharField(required=True, label="RUT gerente",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'oninput': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': '987654321',})
                          )
    nombre_gerente = forms.CharField(required=True, label="Nombre Gerente",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    direccion_gerente = forms.CharField (required=True, label="direccion gerente",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    telefono = forms.CharField(required=True, label="Teléfono",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': "form-control"}))
    gratificacion = forms.ModelChoiceField(queryset=Gratificacion.objects.all(), required=True, label="Gratificacion",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True, label="region",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.all(), required=True, label="ciudad",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(), required=True, label="provincia",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    bono = forms.ModelMultipleChoiceField(queryset=Bono.objects.all(), required=True, label="Bonos",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick form-control',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )
    examen = forms.ModelMultipleChoiceField(queryset=Examen.objects.all(), required=True, label="Examenes",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick form-control',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )

    def __init__(self, *args, **kwargs):
        Planta = kwargs.pop('planta', None)
        super(PlantaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('negocio', css_class='form-group col-md-6 mb-0'),
                Column('rut', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nombre', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('region', css_class='form-group col-md-4 mb-0'),
                Column('provincia', css_class='form-group col-md-4 mb-0'),
                Column('ciudad', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('direccion', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nombre_gerente', css_class='form-group col-md-6 mb-0'),
                Column('rut_gerente', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('direccion_gerente', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('gratificacion', css_class='form-group col-md-6 mb-0'),
                Column('bono', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),         

        )

    class Meta:
        model = Planta
        fields = ('rut','nombre', 'rut_gerente','nombre_gerente', 'direccion_gerente', 'telefono', 'email', 'negocio', 'gratificacion', 'bono', 'region', 'provincia', 'ciudad', 'direccion')


class SaludForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(SaludForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Salud
        fields = ("nombre",)


class AfpForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    tasa = forms.IntegerField(required=True, label="Tasa",
                                 widget=forms.NumberInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AfpForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Afp
        fields = ("nombre", "tasa",)


class ValoresDiarioForm(forms.ModelForm):
    valor_diario = forms.CharField(required=True, label="Valor Diario",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(ValoresDiarioForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ValoresDiario
        fields = ("valor_diario",)


class ValoresDiarioAfpForm(forms.ModelForm):
    valor = forms.CharField(required=True, label="Valor",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
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
