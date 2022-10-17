from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.validators import RegexValidator
from django.forms import model_to_dict
# Crum User
from crum import get_current_user
from utils.models import Area, Cargo, Horario, Gratificacion, Bono,Region, Provincia, Ciudad 

# Create your models here.



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
    razon_social = models.CharField(verbose_name="Razón Social", max_length=100)
    giro = models.CharField(max_length=150, blank=True, null=True)
    abreviatura = models.CharField(max_length=4)
    email = models.EmailField(
        'correo',
        unique=True,
        blank=True,
        null=True,
        max_length=50,
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
        'Área',
        help_text='Seleccione uno o mas área para este cliente.'
    )

    cargo = models.ManyToManyField(
        Cargo,
        help_text='Seleccione uno o mas cargo para este cliente.'
    )

    horario = models.ManyToManyField(
        Horario,
        help_text='Seleccione uno o mas horario para este cliente.'
    )
    region = models.ForeignKey(Region, verbose_name="Región", on_delete=models.SET_NULL, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(
        verbose_name="Dirección",
        max_length=200
    )
    cod_uny_cliente = models.CharField(
        max_length=240,
        null=True,
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el cliente, deshabilite esta casilla.'
    )

    def __str__(self):
        return self.razon_social

    def toJSON(self):
        item = model_to_dict(self)
        return item


class Negocio(BaseModel):
    """Negocio model.

    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    archivo = models.FileField(
        upload_to='archivo_negocio/',
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg', ])]
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la Negocio, deshabilite esta casilla.'
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
        item['archivo'] = str(self.archivo).zfill(0)
        return item


class Planta(models.Model):
    """Modelo Planta.
    """ 
    rut_regex = RegexValidator(
        regex=r'^[0-9]{7,9}[0-9kK]{1}$',
        message='El RUT debe ser valido. Ingresalo sin puntos ni guiones.'
    )

    rut = models.CharField(
        max_length=12,
        # validators=[rut_regex, ],

        error_messages={
            'unique': 'Ya existe una planta con este RUT registrado.'
        }
    )
    nombre = models.CharField(max_length=100)

    rut_gerente = models.CharField(
        verbose_name="Rut Gerente",
        max_length=12
    )
    nombre_gerente = models.CharField(verbose_name="Nombre Gerente", max_length=100)

    direccion_gerente = models.CharField(
        'Dirección Gerente',
        max_length=200,
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
    email = models.EmailField(
        'email address',
        null=True,
        blank=True,
        max_length=50,
        error_messages={
            'unique': 'Ya existe un negocio con este email registrado.'
        }
    )
    cod_uny_planta = models.CharField(
        max_length=240,
        null=True,
    )
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)

    cliente = models.ForeignKey(Cliente, related_name='championed_by', on_delete=models.CASCADE)

    region = models.ForeignKey(Region, verbose_name="Región", on_delete=models.SET_NULL, null=True)

    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)

    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)

    direccion = models.CharField(
        max_length=200,
    )

    bono = models.ManyToManyField(
        Bono,
        blank=True,
        help_text='Seleccione una o mas Bonos para esta planta.'
    )

    gratificacion = models.ForeignKey(Gratificacion, verbose_name="Gratificación", on_delete=models.SET_NULL, null=True)

    masso = models.BooleanField(
        default=False,
        help_text='Si charla Masso es requerido, habilite esta casilla.'
    )

    psicologico = models.BooleanField(
        verbose_name="Psicológico",
        default=False,
        help_text='Si el tipo de examen psicológico es requerido, habilite esta casilla.'
    )

    hal2 = models.BooleanField(
        default=False,
        help_text='Si examen hal2 es requerido, habilite esta casilla.'
    )

    bateria = models.ForeignKey("examenes.Bateria", verbose_name="Batería", on_delete=models.PROTECT, null=True, blank=True)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar la planta, deshabilite esta casilla.'
    )

    def __str__(self):
        """Return RUT."""
        return self.nombre

    def get_short_name(self):
        """Return RUT."""
        return self.rut_gerente
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        item['codigo'] = self.cod_uny_planta
        item['negocio'] = self.negocio.nombre.title()
        item['negocio_id'] = self.negocio.id
        item['region_id'] = self.region.id
        item['provincia_id'] = self.provincia.id
        item['ciudad_id'] = self.ciudad.id
        item['bono'] =  [t.toJSON() for t in self.bono.all()]
        return item


class ContactoPlanta(models.Model):
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
    rut = models.CharField(
        max_length=12,
        unique=True,
        error_messages={
            'unique': 'Ya existe un Contacto Planta con este RUT registrado.'
        }
    )
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

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
        'Correo',
        null=True,
        blank=True,
        max_length=50,
        error_messages={
            'unique': 'Ya existe un Contacto Planta con este email registrado.'
        }
    )
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', null=True, blank=True)

    relacion = models.CharField('Relación', max_length=3, choices=RELACION_PLANTA)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )
    planta = models.ForeignKey(
        Planta,
        on_delete=models.CASCADE
        # help_text='Seleccione solo una planta si el perfil que esta seleccionado es Trabajador.'
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    status = models.BooleanField(
        default=True,
        help_text='Para desactivar el Contacto de esta Planta, deshabilite esta casilla.'
    )

    def __str__(self):
        """Return Nombres."""
        return self.nombres
    
    def toJSON(self):
        item = model_to_dict(self)
        item['user_id'] = self.user.id
        item['user_rut'] = self.user.rut
        # item['user'] = self.user.first_name +' '+ self.user.last_name
        item['planta_id'] = self.planta.id
        item['planta'] = self.planta.nombre
        item['cliente'] = self.cliente.razon_social
        return item
