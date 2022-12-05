"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
# Utilities
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from clientes.models import Planta

# Models
from users.models import User, Trabajador, Sexo, Civil, Nacionalidad, Salud, Afp, ValoresDiario, ValoresDiarioAfp, Banco, TipoCta, NivelEstudio, Especialidad, TipoArchivo, ArchivoTrabajador, ListaNegra, Profesion, ProfesionTrabajador, Parentesco, Contacto
# sexo, estado_civil, fecha_nacimiento, telefono, nacionalidad, domicilio,
# planta, sistema_salud, sistema_prevision, banco, tipo_cta, cuenta


class SexoSetResource(resources.ModelResource):

    class Meta:
        model = Sexo
        fields = ('id', 'nombre', 'status', )


class CivilSetResource(resources.ModelResource):

    class Meta:
        model = Civil
        fields = ('id', 'nombre', 'status', )


class NacionalidadSetResource(resources.ModelResource):

    class Meta:
        model = Nacionalidad
        fields = ('id', 'nombre', 'status', )


class SaludSetResource(resources.ModelResource):

    class Meta:
        model = Salud
        fields = ('id', 'nombre', 'status', )


class AfpSetResource(resources.ModelResource):

    class Meta:
        model = Afp
        fields = ('id', 'nombre', 'tasa', 'status', )


class ValoresDiarioSetResource(resources.ModelResource):

    class Meta:
        model = ValoresDiario
        fields = ('id', 'valor_diario', 'status', )


class ValoresDiarioAfpSetResource(resources.ModelResource):
    afp = fields.Field(column_name='afp', attribute='afp', widget=ForeignKeyWidget(Afp, 'nombre'))
    valores_diario = fields.Field(column_name='valores_diario', attribute='valores_diario', widget=ForeignKeyWidget(ValoresDiario, 'nombre'))

    class Meta:
        model = ValoresDiarioAfp
        fields = ('id', 'valor', 'afp', 'valores_diario', 'status', )


class NivelEstudioSetResource(resources.ModelResource):

    class Meta:
        model = NivelEstudio
        fields = ('id', 'nombre', 'status', )


class EspecialidadSetResource(resources.ModelResource):

    class Meta:
        model = Especialidad
        fields = ('id', 'nombre', 'status', )


class BancoSetResource(resources.ModelResource):

    class Meta:
        model = Banco
        fields = ('id', 'codigo', 'nombre', 'status', )


class TipoCtaSetResource(resources.ModelResource):

    class Meta:
        model = TipoCta
        fields = ('id', 'nombre', 'status', )


class TipoArchivoSetResource(resources.ModelResource):

    class Meta:
        model = TipoArchivo
        fields = ('id', 'nombre', 'status', )


class UserSetResource(resources.ModelResource):
    groups = fields.Field(column_name='groups', attribute='groups', widget=ForeignKeyWidget(Group, 'name'))

    class Meta:
        model = User
        fields = ['id', 'rut', 'first_name', 'last_name', 'codigo', 'username', 'email', 'telefono',
                  'is_active', 'cambiar_clave', 'created_at', 'created', 'modified_at', 'modified', ]


class TrabajadorSetResource(resources.ModelResource):
    sexo = fields.Field(column_name='sexo', attribute='sexo', widget=ForeignKeyWidget(Sexo, 'nombre'))

    class Meta:
        model = Trabajador
        fields = ['id', 'rut', 'first_name', 'last_name', 'email', 'telefono', ]


class ArchivoTrabajadorSetResource(resources.ModelResource):
    trabajador = fields.Field(column_name='trabajador', attribute='trabajador', widget=ForeignKeyWidget(Trabajador, 'nombre'))
    tipo_archivo = fields.Field(column_name='tipo_archivo', attribute='tipo_archivo', widget=ForeignKeyWidget(TipoArchivo, 'nombre'))

    class Meta:
        model = ArchivoTrabajador
        fields = ('id', 'trabajador', 'tipo_archivo', 'archivo', 'status', )


class ListaNegraSetResource(resources.ModelResource):
    trabajador = fields.Field(column_name='trabajador', attribute='trabajador', widget=ForeignKeyWidget(Trabajador, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))

    class Meta:
        model = ListaNegra
        fields = ('id', 'tipo', 'descripcion', 'trabajador', 'planta', 'status', )


class ProfesionSetResource(resources.ModelResource):

    class Meta:
        model = Profesion
        fields = ('id', 'nombre', 'status', )


class ProfesionTrabajadorSetResource(resources.ModelResource):
    trabajador = fields.Field(column_name='trabajador', attribute='trabajador', widget=ForeignKeyWidget(Trabajador, 'first_name'))
    profesion = fields.Field(column_name='profesion', attribute='profesion', widget=ForeignKeyWidget(Profesion, 'nombre'))

    class Meta:
        model = ProfesionTrabajador
        fields = ('id', 'egreso', 'institucion', 'trabajador', 'profesion', 'status', )


class ParentescoSetResource(resources.ModelResource):

    class Meta:
        model = Parentesco
        fields = ('id', 'nombre', 'status', )


class ContactoSetResource(resources.ModelResource):
    trabajador = fields.Field(column_name='trabajador', attribute='trabajador', widget=ForeignKeyWidget(Trabajador, 'nombre'))
    parentesco = fields.Field(column_name='parentesco', attribute='parentesco', widget=ForeignKeyWidget(Parentesco, 'nombre'))

    class Meta:
        model = Contacto
        fields = ('id', 'nombre', 'telefono', 'trabajador', 'parentesco', 'status', )


@admin.register(Sexo)
class SexoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """SexoAdmin model admin."""

    resource_class = SexoSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(Civil)
class CivilAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """CivilAdmin model admin."""

    resource_class = CivilSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(Nacionalidad)
class NacionalidadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """NacionalidadAdmin model admin."""

    resource_class = NacionalidadSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(Salud)
class SaludAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """SaludAdmin model admin."""

    resource_class = SaludSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(Afp)
class AfpAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """AfpAdmin model admin."""

    resource_class = AfpSetResource
    fields = ('nombre', 'tasa', 'status', )
    list_display = ('id', 'nombre', 'tasa', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(ValoresDiario)
class ValoresDiarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ValoresDiarioAdmin model admin."""

    resource_class = ValoresDiarioSetResource
    fields = ('valor_diario', 'status', )
    list_display = ('id', 'valor_diario', 'status', 'created_date',)
    search_fields = ['valor_diario', ]


@admin.register(ValoresDiarioAfp)
class ValoresDiarioAfpAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ValoresDiarioAfpAdmin model admin."""

    resource_class = ValoresDiarioAfpSetResource
    fields = ('valor', 'afp', 'valor_diario', 'status', )
    list_display = ('id', 'valor', 'afp', 'valor_diario', 'status', 'created_date',)
    list_filter = ['afp', 'valor_diario', ]
    search_fields = ['tipo', 'afp__nombre', 'valor_diario', ]


@admin.register(NivelEstudio)
class NivelEstudioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """NivelEstudioAdmin model admin."""

    resource_class = NivelEstudioSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(Especialidad)
class EspecialidadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """EspecialidadAdmin model admin."""

    resource_class = EspecialidadSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(Banco)
class BancoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """BancoAdmin model admin."""

    resource_class = BancoSetResource
    fields = ('codigo', 'nombre', 'status', )
    list_display = ('id', 'codigo', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(TipoCta)
class TipoCtaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """TipoCtaAdmin model admin."""

    resource_class = TipoCtaSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(TipoArchivo)
class TipoArchivoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """TipoArchivoAdmin model admin."""

    resource_class = TipoArchivoSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    """User model admin."""

    resource_class = UserSetResource
    fieldsets = UserAdmin.fieldsets + (
        ('Más Información', {
            'fields': ('rut', 'fecha_nacimiento', 'telefono', 'cliente', 'planta', 'cambiar_clave', 'atributos', )
        }),
    )
    list_display = ('id', 'groups_list', 'rut', 'first_name', 'last_name', 'is_active')
    list_filter = ('planta', 'groups', 'is_staff', 'created', 'modified')
    search_fields = ('first_name', 'last_name', 'email', 'rut', 'groups__name', 'cliente__razon_social', 'planta__nombre')

    def groups_list(self, obj):
        return u", ".join(o.name for o in obj.groups.all())


@admin.register(Trabajador)
class CustomTrabajadorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """Trabajador model admin."""

    resource_class = TrabajadorSetResource
    fields = ('rut', 'first_name', 'last_name', 'pasaporte', 'sexo', 'estado_civil', 'fecha_nacimiento', 'telefono', 'nacionalidad',
              'licencia_conducir', 'talla_polera', 'talla_pantalon', 'calzado', 'nivel_estudio', 'especialidad',
              'region', 'provincia', 'ciudad', 'domicilio', 'examen', 'foto', 'afp', 'salud', 'pacto_uf', 'banco',
              'tipo_cuenta', 'cuenta', 'terminos_condiciones', 'user')
    list_display = ('id', 'rut', 'first_name', 'last_name', 'telefono', 'nacionalidad')
    list_filter = ('rut', 'provincia', 'ciudad', 'created', 'modified')
    search_fields = ('rut', 'first_name', 'last_name', 'pasaporte', 'region__nombre', 'provincia__nombre', 'ciudad__nombre')


@admin.register(ArchivoTrabajador)
class ArchivoTrabajadorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ArchivoTrabajadorAdmin model admin."""

    resource_class = ArchivoTrabajadorSetResource
    fields = ('trabajador', 'tipo_archivo', 'archivo', 'status', )
    list_display = ('id', 'trabajador', 'tipo_archivo', 'status', 'created_date',)
    list_filter = ['trabajador', 'tipo_archivo', ]
    search_fields = ['trabajador', 'tipo_archivo', 'archivo', ]


@admin.register(ListaNegra)
class ListaNegraAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ListaNegraAdmin model admin."""

    resource_class = ListaNegraSetResource
    fields = ('tipo', 'descripcion', 'trabajador', 'planta', 'status', )
    list_display = ('id', 'tipo', 'descripcion', 'trabajador', 'planta', 'status',)
    list_filter = ['trabajador', 'planta', ]
    search_fields = ['tipo', 'trabajador__rut', 'planta__nombre', ]


@admin.register(Profesion)
class ProfesionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ProfesionAdmin model admin."""

    resource_class = ProfesionSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(ProfesionTrabajador)
class ProfesionTrabajadorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ProfesionTrabajadorAdmin model admin."""

    resource_class = ProfesionTrabajadorSetResource
    fields = ('egreso', 'institucion', 'trabajador', 'profesion', 'status', )
    list_display = ('id', 'institucion', 'egreso', 'trabajador', 'profesion', 'status', 'created_date',)
    list_filter = ['trabajador', 'profesion', ]
    search_fields = ('institucion', 'trabajador', 'profesion__nombre')


@admin.register(Parentesco)
class ParentescoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ParentescoAdmin model admin."""

    resource_class = ParentescoSetResource
    fields = ('nombre', 'status', )
    list_display = ('id', 'nombre', 'status', 'created_date',)
    search_fields = ['nombre', ]


@admin.register(Contacto)
class ContactoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ContactoAdmin model admin."""

    resource_class = ContactoSetResource
    fields = ('nombre', 'telefono', 'trabajador', 'parentesco', 'status', )
    list_display = ('id', 'nombre', 'trabajador', 'parentesco', 'status', 'created_date',)
    list_filter = ['trabajador', 'parentesco', ]
    search_fields = ['nombre', 'trabajador__rut', 'parentesco__nombre', ]


admin.site.register(User, CustomUserAdmin)