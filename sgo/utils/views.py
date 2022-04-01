from django.shortcuts import render

# Create your views here.
"""Utils Views. """

from django.db.models import Count
# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, F, ProtectedError
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
# Forms
from utils.forms import AreaForm, CargoForm, HorarioForm, BonoForm, SaludForm, AfpForm, ValoresDiarioForm, ValoresDiarioAfpForm
from clientes.forms import CrearClienteForm, EditarClienteForm, NegocioForm, PlantaForm


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count
# Modelo
from utils.models import Area, Cargo, Horario, Bono, Region
from clientes.models import Cliente, Negocio, Planta
from ficheros.models import Fichero
from contratos.models import Contrato
from users.models import User, Salud, Afp, ValoresDiario, ValoresDiarioAfp


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        # Obtengo las plantas del Usuario
        plantas = self.request.user.planta.all()
        # Obtengo los ficheros de las plantas a las que pertenece el usuario
        # context['ficheros'] = Fichero.objects.filter(
        #     plantas__in=plantas, status=True
        # ).distinct()
        # Obtengo los contratos del usuario si no es administrador.
        if not self.request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT']).exists():
            context['contratos'] = Contrato.objects.filter(
                user=self.request.user).order_by('modified')
        else:
            # Obtengo todos los contratos por firmar de todas las plantas a las
            # que pertenece el usuario.
            context['contratos'] = Contrato.objects.filter(
                user__planta__in=plantas, estado_firma=Contrato.POR_FIRMAR)

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
            plantas__in=plantas, status=True
        ).distinct()
        # Obtengo los contratos del usuario si no es administrador.
        if not self.request.user.groups.filter(name__in=['Administrador']).exists():
            context['contratos'] = Contrato.objects.filter(
                usuario=self.request.user).order_by('modified')
        else:
            # Obtengo todos los contratos por firmar de todas las plantas a las
            # que pertenece el usuario.
            context['contratos'] = Contrato.objects.filter(
                user__planta__in=plantas, estado_firma=Contrato.POR_FIRMAR)
            context['result'] = Contrato.objects.values(
                'created_by_id','created_by__first_name','created_by__last_name', 'user__planta__nombre').order_by('user__planta').annotate(count=Count('user__planta'))
            estado_firma="FIRMADO_TRABAJADOR"
            context['ft'] = Contrato.objects.values(
                'user__planta__nombre').filter(estado_firma=Contrato.FIRMADO_TRABAJADOR).order_by('user__planta').annotate(count=Count('estado_firma'))

        return context


class AreaView(TemplateView):
    template_name = 'utils/area_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Area.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                area = Area()
                area.nombre = request.POST['nombre'].lower()
                area.status = True
                # espec.created_date = request.POST['created_date']
                area.save()
            elif action == 'edit':
                area = Area.objects.get(pk=request.POST['id'])
                area.nombre = request.POST['nombre'].lower()
                area.save()
            elif action == 'delete':
                area = Area.objects.get(pk=request.POST['id'])
                area.status = False
                area.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Areas'
        context['list_url'] = reverse_lazy('utils:area')
        context['entity'] = 'Areas'
        context['form'] = AreaForm()
        return context


class CargoView(TemplateView):
    template_name = 'utils/cargo_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cargo.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                cargo = Cargo()
                cargo.nombre = request.POST['nombre'].lower()
                cargo.alias = request.POST['alias'].lower()
                cargo.descripcion = request.POST['descripcion']
                cargo.nombre_alias = request.POST['nombre']+request.POST['alias']
                cargo.status = True
                # espec.created_date = request.POST['created_date']
                cargo.save()
            elif action == 'edit':
                cargo = Cargo.objects.get(pk=request.POST['id'])
                cargo.nombre = request.POST['nombre'].lower()
                cargo.alias = request.POST['alias'].lower()
                cargo.descripcion = request.POST['descripcion']
                cargo.nombre_alias = request.POST['nombre']+request.POST['alias']
                cargo.save()
            elif action == 'delete':
                cargo = Cargo.objects.get(pk=request.POST['id'])
                cargo.status = False
                cargo.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cargos'
        context['list_url'] = reverse_lazy('utils:cargo')
        context['entity'] = 'Cargos'
        context['form'] = CargoForm()
        return context
    
class HorarioView(TemplateView):
    template_name = 'utils/horario_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Horario.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                horario = Horario()
                horario.nombre = request.POST['nombre'].lower()
                horario.descripcion = request.POST['descripcion']
                horario.status = True
                # espec.created_date = request.POST['created_date']
                horario.save()
            elif action == 'edit':
                horario = Horario.objects.get(pk=request.POST['id'])
                horario.nombre = request.POST['nombre'].lower()
                horario.descripcion = request.POST['descripcion']
                horario.save()
            elif action == 'delete':
                horario = Horario.objects.get(pk=request.POST['id'])
                horario.status = False
                horario.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Horarios'
        context['list_url'] = reverse_lazy('utils:horario')
        context['entity'] = 'Horarios'
        context['form'] = HorarioForm()
        return context

class BonoView(TemplateView):
    template_name = 'utils/bono_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Bono.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                bono = Bono()
                bono.nombre = request.POST['nombre'].lower()
                bono.alias = request.POST['alias'].lower()
                bono.descripcion = request.POST['descripcion']
                bono.nombre_alias = request.POST['nombre']+request.POST['alias']
                bono.status = True
                # espec.created_date = request.POST['created_date']
                bono.save()
            elif action == 'edit':
                bono = Bono.objects.get(pk=request.POST['id'])
                bono.nombre = request.POST['nombre'].lower()
                bono.alias = request.POST['alias'].lower()
                bono.descripcion = request.POST['descripcion']
                bono.nombre_alias = request.POST['nombre']+request.POST['alias']
                bono.save()
            elif action == 'delete':
                bono = Bono.objects.get(pk=request.POST['id'])
                bono.status = False
                bono.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Bonos'
        context['list_url'] = reverse_lazy('utils:bono')
        context['entity'] = 'Bonos'
        context['form'] = BonoForm
        return context


class SaludView(TemplateView):
    template_name = 'utils/salud_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Salud.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                salud = Salud()
                salud.nombre = request.POST['nombre'].lower()
                salud.status = True
                # espec.created_date = request.POST['created_date']
                salud.save()
            elif action == 'edit':
                salud = Salud.objects.get(pk=request.POST['id'])
                salud.nombre = request.POST['nombre'].lower()
                salud.save()
            elif action == 'delete':
                salud = Salud.objects.get(pk=request.POST['id'])
                salud.status = False
                salud.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Sistema de Salud'
        context['list_url'] = reverse_lazy('utils:salud')
        context['entity'] = 'Salud'
        context['form'] = SaludForm()
        return context


class AfpView(TemplateView):
    template_name = 'utils/afp_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Afp.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                previs = Afp()
                previs.nombre = request.POST['nombre'].lower()
                previs.tasa = request.POST['tasa']
                previs.status = True
                # espec.created_date = request.POST['created_date']
                previs.save()
            elif action == 'edit':
                previs = Afp.objects.get(pk=request.POST['id'])
                previs.nombre = request.POST['nombre'].lower()
                previs.tasa = request.POST['tasa']
                previs.save()
            elif action == 'delete':
                previs = Afp.objects.get(pk=request.POST['id'])
                previs.status = False
                previs.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Sistema de Previsión'
        context['list_url'] = reverse_lazy('utils:afp')
        context['entity'] = 'Afps'
        context['form'] = AfpForm()
        return context


class ValoresDiarioView(TemplateView):
    template_name = 'utils/valores_diario_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in ValoresDiario.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                vdiario = ValoresDiario()
                vdiario.valor_diario = request.POST['valor_diario']
                vdiario.status = True
                vdiario.save()
            elif action == 'edit':
                vdiario = ValoresDiario.objects.get(pk=request.POST['id'])
                vdiario.valor_diario = request.POST['valor_diario']
                vdiario.save()
            elif action == 'delete':
                vdiario = ValoresDiario.objects.get(pk=request.POST['id'])
                vdiario.status = False
                vdiario.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Valores Diarios'
        context['list_url'] = reverse_lazy('utils:valores-diarios')
        context['entity'] = 'ValoresDiario'
        context['form'] = ValoresDiarioForm()
        return context


class ValoresDiarioAfpView(TemplateView):
    template_name = 'utils/vdiario_afp_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in ValoresDiarioAfp.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                vdafp = ValoresDiarioAfp()
                vdafp.valor = request.POST['valor']
                vdafp.afp_id = request.POST['afp']
                vdafp.valor_diario_id = request.POST['valor_diario']
                vdafp.status = True
                # espec.created_date = request.POST['created_date']
                vdafp.save()
            elif action == 'edit':
                vdafp = ValoresDiarioAfp.objects.get(pk=request.POST['id'])
                vdafp.valor = request.POST['valor']
                vdafp.afp_id = request.POST['afp']
                vdafp.valor_diario_id = request.POST['valor_diario']
                vdafp.save()
            elif action == 'delete':
                vdafp = ValoresDiarioAfp.objects.get(pk=request.POST['id'])
                vdafp.status = False
                vdafp.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Valores Diarios AFP'
        context['list_url'] = reverse_lazy('utils:vdiarios_afp')
        context['entity'] = 'ValoresDiario'
        context['form'] = ValoresDiarioAfpForm()
        return context
