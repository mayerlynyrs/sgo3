from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.forms import model_to_dict

# Create your models here.
# Crum User
from crum import get_current_user
from smart_selects.db_fields import GroupedForeignKey



class BaseModel(models.Model):
    """Project base model.

    BaseModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + created_by (User Model): Store the user to created the object.
        + modified (DateTime): Store the last datetime the object was modified.
        + madified_by (User Model): Store the user to modified the object.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on  which the object was created.'
    )
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_created_by",
        blank=True,
        null=True,
        default=None
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on  which the object was last modified.'
    )
    modified_by = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_modified_by",
        blank=True,
        null=True,
        default=None
    )

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
            self.modified_by = user
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        """Meta option."""

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']


class Region(models.Model):
    """Modelo Region.
    """
    nombre = models.CharField(max_length=250)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la region, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    """Modelo Provincia.
    """

    
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=250)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la provincia, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    """Modelo Ciudad.
    """


    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=250)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la ciudad, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre

class Bono(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    descripcion = models.TextField(blank=True, null=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el bono, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
        default= timezone.now,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        return item


class Gratificacion(models.Model):
    """Modelo Gratificacion.
    """


    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(blank=True, null=True)
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la gratificacion, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre

class Cargo(models.Model):
    """Modelo Cargo.
    """

    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    descripcion = models.CharField(
        max_length=300,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este cargo, deshabilite esta casilla.'
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
        return item
    
    


class Area(models.Model):
    """Modelo Area.
    """

    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el area, deshabilite esta casilla.'
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
        return item


class Horario(models.Model):
   
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True, null=True)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el Horario, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
        default= timezone.now,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

class Cliente(BaseModel):
    """Modelo Cliente. """

    # codigo = models.CharField(
    #     'código',
    #     help_text='Identificador único de sistema de gestión.',
    #     max_length=6,
    #     unique=True,
    #     blank=True,
    #     null=True
    # )
    rut = models.CharField(
        max_length=12,
        unique=True,
        error_messages={
            'unique': 'Ya existe un cliente con este RUT registrado.'
        }
    )
    razon_social = models.CharField(max_length=100)
    giro = models.CharField(max_length=150)
    email = models.EmailField(
        'correo',
        unique=True,
        error_messages={
            'unique': 'Ya existe un cliente con este email registrado.'
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
    area = models.ManyToManyField(
        Area,
        help_text='Seleccione uno o mas area para este cliente.'
    )

    cargo = models.ManyToManyField(
        Cargo,
        help_text='Seleccione uno o mas cargo para este cliente.'
    )

    horario = models.ManyToManyField(
        Horario,
        help_text='Seleccione uno o mas horario para este cliente.'
    )

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True) 
    provincia = GroupedForeignKey(Provincia, "region", on_delete=models.SET_NULL, null=True, blank=True)
    ciudad = GroupedForeignKey(Ciudad, "provincia", null=True, blank=True)
    # region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    # provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, blank=True)
    # ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)
    direccion = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el cliente, deshabilite esta casilla.'
    )

    def __str__(self):
        return self.razon_social


class Negocio(BaseModel):
    """Negocio model.

    """

    nombre = models.CharField(max_length=100)

    rut_regex = RegexValidator(
        regex=r'^[0-9]{7,9}[0-9kK]{1}$',
        message='El RUT debe ser valido. Ingresalo sin puntos ni guiones.'
    )

    rut_gerente = models.CharField(
        max_length=12,
        # validators=[rut_regex, ],
        unique=True,
        error_messages={
            'unique': 'Ya existe un negocio con este RUT registrado.'
        }
    )
    nombre_gerente = models.CharField(max_length=100)

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
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'Ya existe un negocio con este email registrado.'
        }
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    gratificacion = models.ForeignKey(Gratificacion, on_delete=models.SET_NULL, null=True, blank=True)

    bono = models.ManyToManyField(
        Bono,
        help_text='Seleccione una o mas Bonos para este negocio.'
    )

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, blank=True)

    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)

    direccion = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el negocio, deshabilite esta casilla.'
    )

    def __str__(self):
        """Return RUT."""
        return self.nombre

    def get_short_name(self):
        """Return RUT."""
        return self.rut_gerente


class Planta(models.Model):
    """Modelo Planta.
    """

    # codigo = models.CharField(
    #     'código',
    #     help_text='Identificador único de sistema de gestión.',
    #     max_length=6,
    #     unique=True,
    #     blank=True,
    #     null=True
    # )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    negocio = models.ManyToManyField(
        Negocio,
        help_text='Seleccione uno o mas negocios para esta planta.'
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la planta, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )

    def __str__(self):
        return self.nombre




class PuestaDisposicion(models.Model):
    nombre = models.CharField(max_length=120)
    gratificacion = models.IntegerField()
    seguro_cesantia = models.FloatField()
    seguro_invalidez = models.FloatField()
    seguro_vida = models.FloatField()
    mutual = models.FloatField()


    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el puesta a disposicion, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
        default= timezone.now,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.nombre


class Abastecimiento(BaseModel):
   
    tipo = models.BooleanField(
        help_text='true.- Habitual false.- No Nabitual.'
    )
    insumos = models.BooleanField(
        help_text='true.- EPP false.- Caja Herramientas.'
    )
    
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el tipo, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
        default= timezone.now,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.nombre


class Equipo(models.Model):

    EPP = 'EPP'
    EPP_ADICIONAL = 'EPPA'
    CAJA_HERRAMIENTAS = 'CJ'
    

    TIPO_EQUIPO = (
        (EPP, 'EPP'),
        (EPP_ADICIONAL, 'EPP Adicionales'),
        (CAJA_HERRAMIENTAS, 'Caja de Herramientas'),
    )
   
    nombre = models.CharField(max_length=120)
    valor = models.IntegerField()
    tipo = models.CharField(max_length=4, choices=TIPO_EQUIPO, default=EPP)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el equipo, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
        default= timezone.now,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.nombre
