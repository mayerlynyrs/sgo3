"""User model."""

import os

# Django
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone

from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

#Utilities
from clientes.models import Cliente, Negocio, Planta
from utils.models import BaseModel, Region, Provincia, Ciudad
from .especialidads import Especialidad


class Sexo(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este sexo, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre


class Civil(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este estado civil, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre


class Nacionalidad(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True,
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar esta nacionalidad, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre


class Salud(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el sistema de salud, deshabilite esta casilla.'
    )
    cod_uny_salud = models.CharField(
        max_length=240,
        null=True,
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        return item


class Afp(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    tasa = models.FloatField()
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la AFP, deshabilite esta casilla.'
    )
    cod_uny_afp = models.CharField(
        max_length=240,
        null=True,
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        return item


class ValoresDiario(models.Model):
    valor_diario = models.IntegerField(
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el valor diario, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return str(self.valor_diario)

    def toJSON(self):
        item = model_to_dict(self)
        return item


class ValoresDiarioAfp(models.Model):
    valor = models.IntegerField()
    afp = models.ForeignKey(Afp, on_delete=models.PROTECT, null=True, blank=True)
    valor_diario = models.ForeignKey(ValoresDiario, on_delete=models.PROTECT, null=True, blank=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el valor diario de la AFP, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return str(self.valor)

    def toJSON(self):
        item = model_to_dict(self)
        item['afp_id'] = self.afp.id
        item['afp'] = self.afp.nombre.title()
        item['valor_diario_id'] = self.valor_diario.id
        item['valor_diario'] = self.valor_diario.valor_diario
        return item


class NivelEstudio(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el nivel de estudio, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre


class Banco(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este banco, deshabilite esta casilla.'
    )
    codigo = models.CharField(
        'código',
        max_length=3,
        unique=True,
        blank=True,
        null=True
    )
    rut = models.CharField(
        max_length=120,
    )

    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre


class TipoCta(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este tipo de cuenta, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre


class TipoArchivo(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el tido de archivo, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre


class User(BaseModel, AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to rut and add some extra fields.
    """
    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    atributos = models.JSONField(blank=True, null=True)
    # atributos = models.JSONField(default={})

    cambiar_clave = models.BooleanField(
        'Cambiar Clave',
        default=True,
        help_text='Marque esta casilla para que el usuario cambie su clave después de ingresar.'
    )

    email = models.EmailField(
        'email address',
        unique=True,
        max_length=50,
        error_messages={
            'unique': 'Ya existe un usuario con este email registrado.'
        }
    )

    cliente = models.ManyToManyField(
        Cliente,
        help_text='Seleccione solo un cliente si el perfil que esta seleccionado es Trabajador.'
    )

    planta = models.ManyToManyField(
        Planta,
        help_text='Seleccione solo una planta si el perfil que esta seleccionado es Trabajador.'
    )

    rut_regex = RegexValidator(
        regex=r'^[0-9]{7,9}[0-9kK]{1}$',
        message='El RUT debe ser valido. Ingresalo sin puntos ni guiones.'
    )

    rut = models.CharField(
        max_length=12,
        # validators=[rut_regex, ],
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este RUT registrado.'
        }
    )

    fecha_nacimiento = models.DateField(null=True, blank=True)

    telefono_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='El numero de telefono debe ser ingresado en el siguiente formato +999999999. Solo puede ingresar hasta 15 digitos.'
    )

    telefono = models.CharField(
        'Teléfono',
        validators=[telefono_regex, ],
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        """Return RUT."""
        return self.first_name + " " + self.last_name + " - " + self.rut

    def get_short_name(self):
        """Return RUT."""
        return self.rut
        # return self.rut + '-' +str(self.foto).zfill(0)

    def toJSON(self):
        item = model_to_dict(self)
        return item
        
    
class Trabajador(BaseModel):
    """Trabajador model.


    """

    NINGUNA = 'NG'
    CLASE_A1 = 'A1'
    CLASE_A2 = 'A2'
    CLASE_A3 = 'A3'
    CLASE_A4 = 'A4'
    CLASE_A5 = 'A5'
    CLASE_B = 'B'
    CLASE_C = 'C'
    CLASE_D = 'D'
    CLASE_E = 'E'
    CLASE_F = 'F'

    LICENCIA_ESTADO = (
        (NINGUNA, 'Ninguna'),
        (CLASE_A1, 'Clase A1'),
        (CLASE_A2, 'Clase A2'),
        (CLASE_A3, 'Clase A3'),
        (CLASE_A4, 'Clase A4'),
        (CLASE_A5, 'Clase A5'),
        (CLASE_B, 'Clase B'),
        (CLASE_C, 'Clase C'),
        (CLASE_D, 'Clase D'),
        (CLASE_E, 'Clase E'),
        (CLASE_F, 'Clase F'),
    )

    rut = models.CharField(
        max_length=12,
        unique=True,
        error_messages={
            'unique': 'Ya existe un trabajador con este RUT registrado.'
        }
    )
    first_name = models.CharField(
        max_length=120,
        unique=True
    )
    last_name = models.CharField(
        max_length=120,
        unique=True
    )

    pasaporte = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        error_messages={
            'unique': 'Ya existe un usuario con este pasaporte registrado.'
        }
    )

    sexo = models.ForeignKey(Sexo, on_delete=models.PROTECT, null=True, blank=True)

    estado_civil = models.ForeignKey(Civil, on_delete=models.PROTECT, null=True, blank=True)

    fecha_nacimiento = models.DateField(null=True, blank=True)

    email = models.EmailField(
        'email address',
        unique=True,
        max_length=50,
        error_messages={
            'unique': 'Ya existe un usuario con este email registrado.'
        }
    )

    telefono_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='El numero de telefono debe ser ingresado en el siguiente formato +999999999. Solo puede ingresar hasta 15 digitos.'
    )

    telefono = models.CharField(
        'Teléfono',
        validators=[telefono_regex, ],
        max_length=15,
        blank=True,
        null=True
    )

    telefono2 = models.CharField(
        'Teléfono',
        validators=[telefono_regex, ],
        max_length=15,
        blank=True,
        null=True
    )

    licencia_conducir = models.CharField(max_length=2, choices=LICENCIA_ESTADO, default=NINGUNA)

    talla_polera = models.CharField(
        max_length=3,
        null=True,
        blank=True
    )

    talla_pantalon = models.CharField(
        max_length=2,
        null=True,
        blank=True
    )
    calzado = models.IntegerField(null=True, blank=True)

    nivel_estudio = models.ForeignKey(NivelEstudio, on_delete=models.PROTECT, null=True, blank=True)

    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT, null=True, blank=True)

    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.PROTECT, null=True, blank=True)

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, blank=True)

    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)

    domicilio = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    examen = models.BooleanField(
        default=False,
        help_text='Para solicitar examen psicológico al usuario, habilite esta casilla.'
    )
    foto = models.ImageField(upload_to='usuarios', null=True, blank=True)

    afp = models.ForeignKey(Afp, on_delete=models.PROTECT, null=True, blank=True)

    salud = models.ForeignKey(Salud, on_delete=models.PROTECT, null=True, blank=True)

    pacto_uf = models.FloatField(null=True, blank=True)

    banco = models.ForeignKey(Banco, on_delete=models.PROTECT, null=True, blank=True)

    tipo_cuenta = models.ForeignKey(TipoCta, on_delete=models.PROTECT, null=True, blank=True)

    cuenta = models.CharField(
        'Número de cuenta',
        max_length=30,
        blank=True,
        unique=True,
        null=True
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    is_active = models.BooleanField(
        default=True,
        help_text='Para desactivar el trabajador, deshabilite esta casilla.'
    )

    def __str__(self):
        """Return RUT."""
        return self.first_name + " " + self.last_name + " - " + self.rut

    def get_short_name(self):
        """Return RUT."""
        return self.rut
        # return self.rut + '-' +str(self.foto).zfill(0)

    def toJSON(self):
        item = model_to_dict(self)
        item['foto'] = str(self.foto).zfill(0)
        return item


class ArchivoTrabajador(models.Model):
    archivo = models.FileField(
        upload_to='archivousuario/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])]
    )
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, null=True, blank=True)
    tipo_archivo = models.ForeignKey(TipoArchivo, on_delete=models.PROTECT, null=True, blank=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el archivo del usuario, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.trabajador.first_name + '-' + self.tipo_archivo.nombre + '-' +str(self.archivo).zfill(0)

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo_archivo'] = self.tipo_archivo.nombre.title()
        item['tipo_archivo_id'] = self.tipo_archivo.id
        item['archivo'] = str(self.archivo).zfill(0)
        return item


class ListaNegra(BaseModel):
    LISTA_NEGRA = 'LN'
    LISTA_NEGRA_PLANTA = 'LNP'

    TIPO_LN = (
        (LISTA_NEGRA, 'Lista Negra'),
        (LISTA_NEGRA_PLANTA, 'Lista Negra por Planta'),
    )
    tipo = models.CharField(max_length=3, choices=TIPO_LN, default=LISTA_NEGRA)
    descripcion = models.TextField('Descripción')
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, null=True)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, null=True, blank=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la lista negra, deshabilite esta casilla.'
    )
    
    def __str__(self):
        return str(self.trabajador)
        
    def toJSON(self):
        item = model_to_dict(self)
        item['trabajador'] = self.trabajador.first_name + " " + self.trabajador.last_name + " - " + self.trabajador.rut
        item['trabajador_id'] = self.trabajador.id
        if(self.planta):
            item['planta'] = self.planta.nombre.title()
            item['planta_id'] = self.planta.id
        else:
            item['planta'] = "No Especificada"

        return item


class Parentesco(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el parentesco, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre


class Contacto(models.Model):
    nombre = models.CharField(
        max_length=120,
    )
    telefono_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='El numero de telefono debe ser ingresado en el siguiente formato +999999999. Solo puede ingresar hasta 15 digitos.'
    )
    telefono = models.CharField(
        'Teléfono',
        validators=[telefono_regex, ],
        max_length=15,
        blank=True,
        null=True
    )
    parentesco = models.ForeignKey(Parentesco, on_delete=models.PROTECT, null=True, blank=True)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.PROTECT, null=True, blank=True)
    # nombre_parentesco_user = models.CharField(
    #     max_length=240,
    #     null=True,
    #     unique=True
    # )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el contacto, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre + '-' + self.parentesco.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        item['parentesco'] = self.parentesco.nombre.title()
        item['parentesco_id'] = self.parentesco.id
        return item
