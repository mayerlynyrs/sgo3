from django.shortcuts import render

# Create your views here.
"""Utils Views. """

from django.db.models import Count
# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from django.db.models import Count
# Modelo
from utils.models import Planta
from ficheros.models import Fichero
from contratos.models import Contrato
from users.models import User


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        # Obtengo las plantas del Usuario
        plantas = self.request.user.planta.all()
        # Obtengo los ficheros de las plantas a las que pertenece el usuario
        context['ficheros'] = Fichero.objects.filter(
            plantas__in=plantas, activo=True
        ).distinct()
        # Obtengo los contratos del usuario si no es administrador.
        if not self.request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT']).exists():
            context['contratos'] = Contrato.objects.filter(
                usuario=self.request.user).order_by('modified')
        else:
            # Obtengo todos los contratos por firmar de todas las plantas a las
            # que pertenece el usuario.
            context['contratos'] = Contrato.objects.filter(
                usuario__planta__in=plantas, estado=Contrato.POR_FIRMAR)

        return context


class Inicio(LoginRequiredMixin, TemplateView):
    template_name = 'inicio.html'

    def get_context_data(self, **kwargs):
        context = super(Inicio, self).get_context_data(**kwargs)
        # Obtengo los datos del Usuario
        context['dusuario'] = User.objects.filter()
        # Obtengo las plantas del Usuario
        plantas = self.request.user.planta.all()
        # Obtengo los ficheros de las plantas a las que pertenece el usuario
        context['ficheros'] = Fichero.objects.filter(
            plantas__in=plantas, activo=True
        ).distinct()
        # Obtengo los contratos del usuario si no es administrador.
        if not self.request.user.groups.filter(name__in=['Administrador']).exists():
            context['contratos'] = Contrato.objects.filter(
                usuario=self.request.user).order_by('modified')
        else:
            # Obtengo todos los contratos por firmar de todas las plantas a las
            # que pertenece el usuario.
            context['contratos'] = Contrato.objects.filter(
                usuario__planta__in=plantas, estado=Contrato.POR_FIRMAR)
            context['result'] = Contrato.objects.values(
                'created_by_id','created_by__first_name','created_by__last_name', 'usuario__planta__nombre').order_by('usuario__planta').annotate(count=Count('usuario__planta'))
            estado="FIRMADO_TRABAJADOR"
            context['ft'] = Contrato.objects.values(
                'usuario__planta__nombre').filter(estado=Contrato.FIRMADO_TRABAJADOR).order_by('usuario__planta').annotate(count=Count('estado'))

# atributos, banco, banco_id, cambiar_clave, ciudad, ciudad_id, cliente, codigo, contrato, contratos_contrato_created_by, contratos_contrato_modified_by, contratos_documentoscontrato_created_by, contratos_documentoscontrato_modified_by, contratos_plantilla_created_by, contratos_plantilla_modified_by, contratos_tipo_created_by, contratos_tipo_modified_by, created, created_by, created_by_id, cuenta, date_joined, domicilio, email, estado_civil, estado_civil_id, fecha_nacimiento, ficheros_fichero_created_by, ficheros_fichero_modified_by, first_name, groups, id, is_active, is_staff, is_superuser, last_login, last_name, logentry, modified, modified_by, modified_by_id, nacionalidad, nacionalidad_id, password, planta, provincia, provincia_id, region, region_id, rut, sexo, sexo_id, sistema_prevision, sistema_prevision_id, sistema_salud, sistema_salud_id, telefono, tipo_cuenta, tipo_cuenta_id, user_permissions, username, users_user_created_by, users_user_modified_by

        return context
