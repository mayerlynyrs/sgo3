"""Requerimiento Forms"""

# Django
from email.policy import default
from tokenize import group
from django import forms
# sgo Model
from users.models import User, Trabajador
from requerimientos.models import Requerimiento, Causal, AreaCargo, RequerimientoTrabajador, Adendum
from clientes.models import Planta, Cliente


class RequerimientoCreateForm(forms.ModelForm):

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

    codigo = forms.CharField(required=False, label="Código",
                             widget=forms.TextInput(attrs={'placeholder': 'Código único del Sistema', 'class': "form-control", 'readonly':'readonly', }))
    centro_costo = forms.CharField(required=True, label="Centro de Costo",
                             widget=forms.TextInput(attrs={'class': "form-control" }))
    nombre = forms.CharField(required=True, label="Nombre Solicitud",
                             widget=forms.TextInput(attrs={'class': "form-control" }))
    fecha_solicitud = forms.CharField(required=True, label="Fecha Solicitud",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_solicitud", 'readonly' :'true'}))                              
    regimen = forms.ChoiceField(choices = REGIMEN_ESTADO, required=True, label="Régimen",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    fecha_inicio = forms.CharField(required=True, label="Fecha Inicio",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_inicio", 'readonly' :'true'}))
    fecha_termino = forms.CharField(required=True, label="Fecha Término",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_termino",'readonly' :'true' }))
    descripcion = forms.CharField (required=True, label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))
    causal = forms.ModelChoiceField(queryset=Causal.objects.all(), required=True, label="Causal",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control','onchange': 'getval(this);' ,
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=True, label="Cliente",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    planta = forms.ModelChoiceField(queryset=Planta.objects.all(), required=True, label="Planta",
                                   widget=forms.Select(attrs={'class': 'show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )


    class Meta:
        model = Requerimiento
        fields = ("codigo", "centro_costo", "nombre", "fecha_solicitud", "regimen", "fecha_inicio", "fecha_termino",
                  "descripcion", "planta","cliente", "causal", )


class ACRForm(forms.ModelForm):
    cantidad = forms.IntegerField(required=True,
                                 widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))
    valor_aprox = forms.FloatField(required=True, label="Valor Aproximado",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'min': 1, 'type': 'number'}))
    fecha_ingreso = forms.CharField(required=True, label="Fecha Ingreso",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off',  'id':"egreso"}))

    area = forms.ModelChoiceField(queryset=Cliente.objects.none(), required=True, label="Área",
                                            widget=forms.Select(
                                                attrs={'class': 'selectpicker show-tick form-control',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )
    cargo = forms.ModelChoiceField(queryset=Cliente.objects.none(), required=True,
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )

    def __init__(self, *args, **kwargs):
        areas = kwargs.pop('areas', None)
        # print(areas)
        cargos = kwargs.pop('cargos', None)
        # print(cargos)
        cantidad = kwargs.pop('cantidad', None)
        # print(cantidad)
        super(ACRForm, self).__init__(*args, **kwargs)
        
        self.fields['area'].queryset = areas
        self.fields['cargo'].queryset = cargos

    class Meta:
        model = AreaCargo
        fields = ("cantidad", "valor_aprox", "fecha_ingreso", "area", "cargo", )


class RequeriTrabajadorForm(forms.ModelForm):

    
    TECNICO = 'TEC'
    SUPERVISOR = 'SUP'

    TIPO_ESTADO = (
        (TECNICO, 'Técnico'),
        (SUPERVISOR, 'Supervisor'),
    )

    descripcion = forms.CharField (required=True, label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))                              
    tipo = forms.ChoiceField(choices=TIPO_ESTADO, required=True, label="Tipo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    pension = forms.CharField(required=False, label="Pensión",
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    area_cargo = forms.ModelChoiceField(queryset=AreaCargo.objects.none(), required=True, label="Área Cargo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.none(), required=True, label="Trabajador",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    jefe_area = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True), required=True, label="Jefe del Área",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        area_cargo = kwargs.pop('area_cargo', None)
        trabajador = kwargs.pop('trab', None)
        total = kwargs.pop('total', None)
        super(RequeriTrabajadorForm, self).__init__(*args, **kwargs)
        self.fields['trabajador'].queryset = trabajador
        self.fields['area_cargo'].queryset = area_cargo

    class Meta:
        model = RequerimientoTrabajador
        fields = ("area_cargo", "tipo", "trabajador", "pension", "jefe_area", "referido", "descripcion", "status")


class ConvenioTrabajadorForm(forms.ModelForm):
    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.none(), required=True,
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )


    def __init__(self, *args, **kwargs):
        trabaj_conve = kwargs.pop('trabaj_conve', None)
        super(ConvenioTrabajadorForm, self).__init__(*args, **kwargs)
        
        self.fields['trabajador'].queryset = trabaj_conve

    class Meta:
        model = RequerimientoTrabajador
        fields = ("trabajador",)


class AdendumForm(forms.ModelForm):
    # fecha_inicio = forms.CharField(required=True, label="Fecha Inicio",
    #                              widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off',  'id':"egreso"}))
    fecha_termino = forms.CharField(required=True, label="Fecha Término",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_termino" }))
                                #  widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_termino",'readonly' :'true' }))

    # requerimiento = forms.ModelChoiceField(queryset=Requerimiento.objects.all(), required=True,
    #                                         widget=forms.Select(
    #                                             attrs={'class': 'selectpicker show-tick form-control',
    #                                                     'type': 'hidden',
    #                                                    'data-size': '5',
    #                                                    'data-live-search': 'true',
    #                                                    'data-live-search-normalize': 'true'
    #                                                    })
    #                                         )

    def __init__(self, *args, **kwargs):
        super(AdendumForm, self).__init__(*args, **kwargs)
        # self.fields['cargo'].queryset = cargos

    class Meta:
        model = Adendum
        fields = ("fecha_termino", )
