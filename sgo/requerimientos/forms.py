"""Requerimiento Forms"""

# Django
from tokenize import group
from django import forms
# sgo Model
from users.models import User
from utils.models import Planta
from requerimientos.models import Requerimiento, Causal, AreaCargo, RequerimientoUser
from utils.models import Planta , Cliente, Area, Cargo


class RequerimientoCreateForm(forms.ModelForm):

    NORMAL = 'NOR'
    PARADA_GENERAL_PLANTA = 'PGP'
    URGENCIA = 'URG'

    REGIMEN_ESTADO = (
        (NORMAL, 'Normal'),
        (PARADA_GENERAL_PLANTA, 'Parada Planta'),
        (URGENCIA, 'Urgencia'),
    )

    codigo = forms.CharField(required=False, label="Código único del Sistema",
                             widget=forms.TextInput(attrs={'class': "form-control", 'readonly':'readonly', }))
    centro_costo = forms.CharField(required=True, label="Centro de Costo",
                             widget=forms.TextInput(attrs={'class': "form-control" }))
    nombre = forms.CharField(required=True, label="Nombre Solicitud",
                             widget=forms.TextInput(attrs={'class': "form-control" }))
    fecha_solicitud = forms.CharField(required=True, label="Fecha Solicitud",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_solicitud", 'readonly' :'true'}))                              
    regimen = forms.ChoiceField(choices = REGIMEN_ESTADO, required=True, label="Regimen",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    fecha_inicio = forms.CharField(required=True, label="Fecha Inicio",
                                 widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete':'off', 'id':"fecha_inicio", 'readonly' :'true'}))
    fecha_termino = forms.CharField(required=True, label="Fecha Termino",
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
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    valor_aprox = forms.FloatField(required=True, label="Valor Aproximado",
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
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
        print(areas)
        cargos = kwargs.pop('cargos', None)
        print(cargos)
        super(ACRForm, self).__init__(*args, **kwargs)
        
        self.fields['area'].queryset = areas
        self.fields['cargo'].queryset = cargos

    class Meta:
        model = AreaCargo
        fields = ("cantidad", "valor_aprox", "fecha_ingreso", "area", "cargo", )


class RequeriUserForm(forms.ModelForm):

    SUPERVISOR = 'SUP'
    TECNICO = 'TEC'

    TIPO_ESTADO = (
        (SUPERVISOR, 'Supervisor'),
        (TECNICO, 'Técnico'),
    )

    descripcion = forms.CharField (required=True, label="Observaciones",
                                 widget=forms.Textarea(attrs={'class': "form-control"}))                              
    tipo = forms.ChoiceField(choices = TIPO_ESTADO, required=True, label="Tipo",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    pension = forms.CharField(required=True, label="Pensión",
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, groups='5'), required=True, label="Trabajador",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    # area_cargo = forms.ModelChoiceField(queryset=AreaCargo.objects.filter(status=True), required=True, label="Área Cargo",
    #                                widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
    #                                                           'data-size': '5',
    #                                                           'data-live-search': 'true',
    #                                                           'data-live-search-normalize': 'true'
    #                                                           })
    #                                )
    jefe_area = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True), required=True, label="Jefe del Área",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RequeriUserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RequerimientoUser
        fields = ("referido", "descripcion", "tipo", "pension", "user", "jefe_area", )
