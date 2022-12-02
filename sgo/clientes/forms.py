"""Clientes Forms"""

# Django
from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

# sgo Model
from clientes.models import Cliente, Negocio, Planta, ContactoPlanta
from utils.models import Area, Cargo, Horario, Bono, Gratificacion, Region, Ciudad, Provincia
from examenes.models import Bateria
from users.models import Salud

User = get_user_model()


class CrearClienteForm(forms.ModelForm):

    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'onblur': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': 'Ingrese RUT sin puntos ni guión',}))
    
    razon_social = forms.CharField(required=True, label="Razón Social",
                             widget=forms.TextInput(attrs={'class': "form-control" }))
    giro = forms.CharField(required=True, label="Giro",
                             widget=forms.TextInput(attrs={'class': "form-control"}))
    cod_uny_cliente = forms.CharField(required=True, label="Código Unysoft",
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
                Column('cod_uny_cliente', css_class='form-group col-md-6 mb-0'),
                Column('horario', css_class='form-group col-md-6 mb-0'),
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
                  "direccion", "region", "provincia", "ciudad", "cod_uny_cliente")
        widgets = {
            'telefono': TextInput(attrs={
                'class': "form-control",
                'type': "number",
                'placeholder': 'Ingrese RUT sin puntos ni guión',
                'maxlength': 12
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
                                    'onblur': "checkRut(this)",
                                    'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                                    'placeholder': 'Ingrese RUT sin puntos ni guión',})
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
    cod_uny_cliente = forms.CharField(required=True, label="Código Unysoft",
                             widget=forms.TextInput(attrs={'class': "form-control"}))
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
                Column('cod_uny_cliente', css_class='form-group col-md-6 mb-0'),
                Column('horario', css_class='form-group col-md-6 mb-0'),
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
                  "direccion", "region", "provincia", "ciudad", "cod_uny_cliente")
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
    descripcion = forms.CharField (required=True, label="Descripción",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))
    archivo = forms.FileField()

    def __init__(self, *args, **kwargs):
        Negocio = kwargs.pop('negocio', None)
        super(NegocioForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Negocio
        fields = ("nombre", "descripcion", "archivo")


class PlantaForm(forms.ModelForm):
    negocio = forms.ModelChoiceField(queryset=Negocio.objects.none(), required=True, label="Negocio",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control ',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    rut = forms.CharField(required=True, label="RUT Planta",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'onblur': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': 'Ingrese RUT sin puntos ni guión',})
                          ) 
    nombre = forms.CharField(required=True, label="Razón Social",
                                 widget=forms.TextInput(attrs={'class': "form-control "}))
    telefono = forms.CharField(required=True, label="Teléfono Planta",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'maxlength': 12}))
    direccion = forms.CharField (required=True, label="Dirección",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    rut_gerente = forms.CharField(required=True, label="RUT Gerente",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'onblur': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': 'Ingrese RUT sin puntos ni guión',})
                          )
    nombre_gerente = forms.CharField(required=True, label="Nombre Gerente",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    direccion_gerente = forms.CharField (required=True, label="Dirección Gerente",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required=True, label="Correo Planta",
                             widget=forms.EmailInput(attrs={'class': "form-control"}))
    gratificacion = forms.ModelChoiceField(queryset=Gratificacion.objects.all(), required=True, label="Gratificación",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    bono = forms.ModelMultipleChoiceField(queryset=Bono.objects.all(), required=False, label="Bonos",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick form-control',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )
    bateria = forms.ModelChoiceField(queryset=Bateria.objects.all(), required=False, label="Batería",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    masso =forms.BooleanField(required=False, label='Masso',
                                 widget=forms.CheckboxInput(attrs={'class': "form-control-lg",
                                                                   }))
    psicologico =forms.BooleanField(required=False, label='Psicológico',
                                 widget=forms.CheckboxInput(attrs={'class': "form-control-lg",
                                                                    'onclick' :"javascript:validar(this)",
                                                                   }))
    hal2 =forms.BooleanField(required=False, label='Hal2',
                                 widget=forms.CheckboxInput(attrs={'class': "form-control-lg",
                                                                   'disabled':'disabled',})) 
    cod_uny_planta = forms.CharField(required=True, label="Código Unysoft",
                                 widget=forms.TextInput(attrs={'class': "form-control "}))


    def __init__(self, *args, **kwargs):
        planta = kwargs.pop('planta', None)
        print('planta', planta)
        cliente_id = kwargs.pop('cliente_id', None)
        print('cliente_id', cliente_id)
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
                Column('bono', css_class='form-group col-md-6 mb-0'),
                Column('gratificacion', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('masso', css_class='form-group col-md-2 mb-0'),
                Column('psicologico', css_class='form-group col-md-2 mb-0'),
                Column('hal2', css_class='form-group col-md-2 mb-0'),
                Column('bateria', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('region2', css_class='form-group col-md-4 mb-0'),
                Column('provincia2', css_class='form-group col-md-4 mb-0'),
                Column('ciudad2', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('direccion', css_class='form-group col-md-6 mb-0'),
                Column('cod_uny_planta', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('rut_gerente', css_class='form-group col-md-6 mb-0'),
                Column('nombre_gerente', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('direccion_gerente', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),         

        )

        if self.fields['negocio'].queryset == 'x1x2x3':
            # if not planta.groups.filter(name='Administrador').exists():
            # self.fields['group'].queryset = Group.objects.exclude(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT', ])
            self.fields['negocio'].queryset = Negocio.objects.filter(id__in=planta.cliente.all())
        else:
            # self.fields['group'].queryset = Group.objects.all()
            self.fields['negocio'].queryset = Negocio.objects.filter(cliente_id=cliente_id)

    class Meta:
        model = Planta
        fields = ('rut','nombre', 'rut_gerente','nombre_gerente', 'direccion_gerente', 'telefono', 'email', 'negocio', 'gratificacion', 'bono', 'region2', 'provincia2', 'ciudad2', 'direccion', 'psicologico', 'hal2', 'cod_uny_planta')


class ContactoPlantaForm(forms.ModelForm):
    GERENTE = 'GTE'
    SUBGERENTE = 'SGT'
    JEFEPLANTA = 'JPT'
    JEFETURNO = 'JTN'
    JEFEDEPART = 'JDP'
    SUPERVISOR = 'SUP'
    OTROS = 'OTR'

    RELACION_PLANTA = (
        (GERENTE, 'Gerente'),
        (SUBGERENTE, 'Sub Gerente'),
        (JEFEPLANTA, 'Jefe Planta'),
        (JEFETURNO, 'Jefe Turno'),
        (JEFEDEPART, 'Jefe Departamento'),
        (SUPERVISOR, 'Supervisor'),
        (OTROS, 'Otros'),
    ) 
    nombres = forms.CharField(required=True, label="Nombres",
                                 widget=forms.TextInput(attrs={'class': "form-control "})) 
    apellidos = forms.CharField(required=True, label="Apellidos",
                                 widget=forms.TextInput(attrs={'class': "form-control "}))
    telefono = forms.CharField(required=True, label="Teléfono",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'maxlength': 12}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': "form-control"}))
    fecha_nacimiento = forms.DateField(required=True, label="Fecha de Nacimiento",
                                widget=forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA','class': "form-control", 'autocomplete':'off', 'id':"fecha"}))
    planta = forms.ModelChoiceField(queryset=Planta.objects.filter(status=True), required=False, label="Planta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )                              
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(status=True), required=False, label="Cliente",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )                            
    relacion = forms.ChoiceField(choices = RELACION_PLANTA, required=True, label="Vínculo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control",
                          'onkeypress': "return isNumber(event)",
                          'onblur': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': 'Ingrese RUT sin puntos ni guión',})
                          )

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user', None)
        # print(user)
        super(ContactoPlantaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('nombres', css_class='form-group col-md-6 mb-0'),
                Column('apellidos', css_class='form-group col-md-6 mb-0'),
                css_class='form-row col-md-12'
            ),
            Row(
                Column('rut', css_class='form-group col-md-4 mb-0'),
                Column('fecha_nacimiento', css_class='form-group col-md-4 mb-0'),          
                Column('relacion', css_class='form-group col-md-4 mb-0'),
                css_class='form-row col-md-12'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row col-md-12'
            ),       

        )

    class Meta:
        model = ContactoPlanta
        fields = ("nombres", "apellidos", "rut", "telefono", "email", "fecha_nacimiento", "planta", "cliente", "relacion", )
