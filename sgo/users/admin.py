"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Utilities
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Models
from users.models import User, Sexo, Civil, Nacionalidad, Salud, Afp, Banco, TipoCta
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
        fields = ('id', 'nombre', 'status', )


class BancoSetResource(resources.ModelResource):

    class Meta:
        model = Banco
        fields = ('id', 'nombre', 'status', )


class TipoCtaSetResource(resources.ModelResource):

    class Meta:
        model = TipoCta
        fields = ('id', 'nombre', 'status', )


class UserSetResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ['id', 'rut', 'first_name', 'last_name', 'codigo', 'username', 'email', 'telefono',
                  'is_active', 'cambiar_clave', 'created_at', 'created', 'modified_at', 'modified', ]


@admin.register(Sexo)
class SexoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """SexoAdmin model admin."""

    resource_class = SexoSetResource
    fields = ('nombre', )
    list_display = ('id', 'nombre', 'status',)
    search_fields = ['nombre', ]


@admin.register(Civil)
class CivilAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """CivilAdmin model admin."""

    resource_class = CivilSetResource
    fields = ('nombre', )
    list_display = ('id', 'nombre', 'status',)
    search_fields = ['nombre', ]


@admin.register(Nacionalidad)
class NacionalidadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """NacionalidadAdmin model admin."""

    resource_class = NacionalidadSetResource
    fields = ('nombre', )
    list_display = ('id', 'nombre', 'status',)
    search_fields = ['nombre', ]


@admin.register(Salud)
class SaludAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """SaludAdmin model admin."""

    resource_class = SaludSetResource
    fields = ('nombre', )
    list_display = ('id', 'nombre', 'status',)
    search_fields = ['nombre', ]


@admin.register(Afp)
class AfpAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """AfpAdmin model admin."""

    resource_class = AfpSetResource
    fields = ('nombre', )
    list_display = ('id', 'nombre', 'status',)
    search_fields = ['nombre', ]


@admin.register(Banco)
class BancoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """BancoAdmin model admin."""

    resource_class = BancoSetResource
    fields = ('nombre', )
    list_display = ('id', 'nombre', 'status',)
    search_fields = ['nombre', ]


@admin.register(TipoCta)
class TipoCtaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """TipoCtaAdmin model admin."""

    resource_class = TipoCtaSetResource
    fields = ('nombre', )
    list_display = ('id', 'nombre', 'status',)
    search_fields = ['nombre', ]


class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    """User model admin."""

    resource_class = UserSetResource
    fieldsets = UserAdmin.fieldsets + (
        ('Más Información', {
            'fields': ('rut', 'sexo', 'estado_civil', 'fecha_nacimiento', 'telefono', 'nacionalidad',
                       'region', 'provincia', 'ciudad', 'domicilio', 'sistema_salud', 'sistema_prevision', 
                       'banco', 'tipo_cuenta', 'cuenta', 'cliente', 'planta', 'cambiar_clave', 'atributos', )
        }),
    )
    list_display = ('id', 'rut', 'first_name', 'last_name', 'email', 'is_active')
    list_filter = ('region', 'provincia', 'ciudad', 'planta', 'is_staff', 'created', 'modified')
    search_fields = ('first_name', 'last_name', 'email', 'rut', 'region__nombre', 'provincia__nombre', 'ciudad__nombre', 'planta__nombre')


admin.site.register(User, CustomUserAdmin)