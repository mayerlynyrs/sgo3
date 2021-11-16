"""User model."""

# Django
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

#Utilities
from utils.models import BaseModel, Cliente, Negocio, Planta, Region, Provincia, Ciudad
# from users import User, Sexo, Civil, Nacionalidad, Salud, Afp, Banco, TipoCta
# atributos, cambiar_clave, codigo, email, rut, sexo, estado_civil, fecha_nacimiento, telefono,
# nacionalidad, domicilio, planta, salud, afp, banco, tipo_cta, cuenta


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
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

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
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

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

class Especialidad(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la especialidad, deshabilite esta casilla.'
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
        error_messages={
            'unique': 'Ya existe un usuario con este email registrado.'
        }
    )

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

    cliente = models.ManyToManyField(
        Cliente,
        help_text='Seleccione solo un cliente si el perfil que esta seleccionado es Trabajador.'
    )

    negocio = models.ManyToManyField(
        Negocio,
        help_text='Seleccione solo una negocio si el perfil que esta seleccionado es Trabajador.'
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

    salud = models.ForeignKey(Salud, on_delete=models.PROTECT, null=True, blank=True)

    afp = models.ForeignKey(Afp, on_delete=models.PROTECT, null=True, blank=True)

    banco = models.ForeignKey(Banco, on_delete=models.PROTECT, null=True, blank=True)

    tipo_cuenta = models.ForeignKey(TipoCta, on_delete=models.PROTECT, null=True, blank=True)

    cuenta = models.CharField(
        'Número de cuenta',
        max_length=30,
        blank=True,
        unique=True,
        null=True
    )

    def __str__(self):
        """Return RUT."""
        return self.rut

    def get_short_name(self):
        """Return RUT."""
        return self.rut

class ArchivoUser(models.Model):
    url = models.FileField(
        upload_to='archivousuario/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])]
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
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
    
    def __int__(self):
        return self.user

class ListaNegra(BaseModel):
    LISTA_NEGRA = 'LN'
    LISTA_NEGRA_PLANTA = 'LNP'

    TIPO_LN = (
        (LISTA_NEGRA, 'Lista Negra'),
        (LISTA_NEGRA_PLANTA, 'Lista Negra por Planta'),
    )
    tipo = models.CharField(max_length=3, choices=TIPO_LN, default=LISTA_NEGRA)
    descripcion = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    planta = models.ForeignKey(Planta, on_delete=models.PROTECT, null=True, blank=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la lista negra, deshabilite esta casilla.'
    )
    
    def __str__(self):
        return str(self.user)

class Profesion(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la profesion, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

class ProfesionUser(models.Model):
    egreso = models.DateField(
        null=True,
        blank=True,
        help_text="Por favor use el siguiente: <em>DD/MM/AAAA</em>."
    )
    institucion = models.CharField(
        max_length=120,
        unique=True
    )
    profesion = models.ForeignKey(Profesion, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la profesion del usuario, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.institucion

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
        unique=True
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
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
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
        return self.nombre
