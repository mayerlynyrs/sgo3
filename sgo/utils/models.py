from django.db import models
from django.utils import timezone
from django.forms import model_to_dict

# Create your models here.
# Crum User
from crum import get_current_user



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
    alias = models.CharField(
        max_length=120,
        default='General'
    )
    descripcion = models.TextField('Descripción', blank=True, null=True)
    nombre_alias = models.CharField(
        max_length=240,
        null=True,
        unique=True
    )
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
        return self.nombre +' - '+ self.alias
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        item['alias'] = self.alias.title()
        return item


class Gratificacion(models.Model):
    """Modelo Gratificacion.
    """

    nombre = models.CharField(max_length=250)
    descripcion = models.TextField('Descripción', blank=True, null=True)
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
        max_length=120
    )
    alias = models.CharField(
        max_length=120,
        default='General'
    )
    descripcion = models.TextField(
        'Descripción',
        max_length=300,
        unique=True
    )
    nombre_alias = models.CharField(
        max_length=240,
        null=True,
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
        return self.nombre +' - '+ self.alias

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre.title()
        item['alias'] = self.alias.title()
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
        help_text='Para desactivar el área, deshabilite esta casilla.'
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


class Horario(models.Model):
   
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField('Descripción', blank=True, null=True)

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
        item['nombre'] = self.nombre.title()
        item['descripcion'] = self.descripcion
        return item


class PuestaDisposicion(models.Model):
    """Modelo Puesta a Disposicion.
    """ 

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
    
    negocio = models.ForeignKey('clientes.Negocio', on_delete=models.CASCADE)

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
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)

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
