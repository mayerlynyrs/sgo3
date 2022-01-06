from django.shortcuts import render

# Create your views here.
"""Utils Views. """

from django.db.models import Count
# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, ProtectedError
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
# Forms
from utils.forms import AreaForm, CargoForm, HorarioForm, BonoForm, CrearClienteForm, NegocioForm, PlantaForm


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from django.db.models import Count
# Modelo
from utils.models import Area, Cargo, Horario, Bono, Negocio, Planta, Cliente, Region
from ficheros.models import Fichero
from contratos.models import Contrato
from users.models import User


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        # Obtengo las negocios del Usuario
        negocios = self.request.user.negocio.all()
        # Obtengo los ficheros de las negocios a las que pertenece el usuario
        context['ficheros'] = Fichero.objects.filter(
            negocios__in=negocios, status=True
        ).distinct()
        # Obtengo los contratos del usuario si no es administrador.
        if not self.request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT']).exists():
            context['contratos'] = Contrato.objects.filter(
                user=self.request.user).order_by('modified')
        else:
            # Obtengo todos los contratos por firmar de todas las negocios a las
            # que pertenece el usuario.
            context['contratos'] = Contrato.objects.filter(
                user__negocio__in=negocios, estado_firma=Contrato.POR_FIRMAR)

        return context


class Inicio(LoginRequiredMixin, TemplateView):
    template_name = 'inicio.html'

    def get_context_data(self, **kwargs):
        context = super(Inicio, self).get_context_data(**kwargs)
        # Obtengo los datos del Usuario
        context['dusuario'] = User.objects.filter()
        # Obtengo las negocios del Usuario
        negocios = self.request.user.negocio.all()
        # Obtengo los ficheros de las negocios a las que pertenece el usuario
        context['ficheros'] = Fichero.objects.filter(
            negocios__in=negocios, status=True
        ).distinct()
        # Obtengo los contratos del usuario si no es administrador.
        if not self.request.user.groups.filter(name__in=['Administrador']).exists():
            context['contratos'] = Contrato.objects.filter(
                usuario=self.request.user).order_by('modified')
        else:
            # Obtengo todos los contratos por firmar de todas las negocios a las
            # que pertenece el usuario.
            context['contratos'] = Contrato.objects.filter(
                usuario__negocio__in=negocios, estado_firma=Contrato.POR_FIRMAR)
            context['result'] = Contrato.objects.values(
                'created_by_id','created_by__first_name','created_by__last_name', 'usuario__negocio__nombre').order_by('usuario__negocio').annotate(count=Count('usuario__negocio'))
            estado_firma="FIRMADO_TRABAJADOR"
            context['ft'] = Contrato.objects.values(
                'usuario__negocio__nombre').filter(estado_firma=Contrato.FIRMADO_TRABAJADOR).order_by('usuario__negocio').annotate(count=Count('estado_firma'))

# atributos, banco, banco_id, cambiar_clave, ciudad, ciudad_id, cliente, codigo, contrato, contratos_contrato_created_by, contratos_contrato_modified_by, contratos_documentoscontrato_created_by, contratos_documentoscontrato_modified_by, contratos_plantilla_created_by, contratos_plantilla_modified_by, contratos_tipo_created_by, contratos_tipo_modified_by, created, created_by, created_by_id, cuenta, date_joined, domicilio, email, estado_civil, estado_civil_id, fecha_nacimiento, ficheros_fichero_created_by, ficheros_fichero_modified_by, first_name, groups, id, is_active, is_staff, is_superuser, last_login, last_name, logentry, modified, modified_by, modified_by_id, nacionalidad, nacionalidad_id, password, negocio, provincia, provincia_id, region, region_id, rut, sexo, sexo_id, sistema_prevision, sistema_prevision_id, sistema_salud, sistema_salud_id, telefono, tipo_cuenta, tipo_cuenta_id, user_permissions, username, users_user_created_by, users_user_modified_by

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
                area.nombre = request.POST['nombre']
                area.status = True
                # espec.created_date = request.POST['created_date']
                area.save()
            elif action == 'edit':
                area = Area.objects.get(pk=request.POST['id'])
                area.nombre = request.POST['nombre']
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
                cargo.nombre = request.POST['nombre']
                cargo.descripcion = request.POST['descripcion']
                cargo.status = True
                # espec.created_date = request.POST['created_date']
                cargo.save()
            elif action == 'edit':
                cargo = Cargo.objects.get(pk=request.POST['id'])
                cargo.nombre = request.POST['nombre']
                cargo.descripcion = request.POST['descripcion']
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
                horario.nombre = request.POST['nombre']
                horario.descripcion = request.POST['descripcion']
                horario.status = True
                # espec.created_date = request.POST['created_date']
                horario.save()
            elif action == 'edit':
                horario = Horario.objects.get(pk=request.POST['id'])
                horario.nombre = request.POST['nombre']
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
                bono.nombre = request.POST['nombre']
                bono.descripcion = request.POST['descripcion']
                bono.status = True
                # espec.created_date = request.POST['created_date']
                bono.save()
            elif action == 'edit':
                bono = Bono.objects.get(pk=request.POST['id'])
                bono.nombre = request.POST['nombre']
                bono.descripcion = request.POST['descripcion']
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

class clienteView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cliente
    template_name = "users/users_list.html"
    paginate_by = 25
    ordering = ['first_name', 'last_name']

    permission_required = 'users.view_user'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(clienteView, self).get_context_data(**kwargs)

        if self.request.user.groups.filter(name__in=['Administrador']).exists():
            institutions = Negocio.objects.values(
                    value=F('id'),
                    title=F('nombre')).all().order_by('nombre')
                #cache.set('institutions', institutions)
            institutions = Sexo.objects.values(
                    value=F('id'),
                    title=F('nombre')).all().order_by('nombre')

            context['negocios'] = institutions
            context['negocio'] = self.kwargs.get('negocio_id', None)

        return context

    def get_queryset(self):
        search = self.request.GET.get('q')
        negocio = self.kwargs.get('negocio_id', None)

        if negocio == '':
            negocio = None

        if search:
            # No es administrador y recibe parametro de busqueda
            if not self.request.user.groups.filter(name__in=['Administrador', ]).exists():
                queryset = User.objects.select_related('negocio').filter(
                    Q(cliente__in=self.request.user.cliente.all()),
                    Q(negocio__in=self.request.user.negocio.all()),
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search) |
                    Q(username__icontains=search)).exclude(
                    groups__name__in=['Administrador']).order_by(
                    'first_name', 'last_name').distinct('first_name', 'last_name')
            else:
                # Es administrador y recibe parametro de busqueda
                queryset = super(clienteView, self).get_queryset().filter(
                                        Q(first_name__icontains=search) |
                                        Q(last_name__icontains=search) |
                                        Q(rut__icontains=search) |
                                        Q(groups__name__icontains=search) |
                                        Q(username__icontains=search)).order_by(
                    'first_name', 'last_name').distinct('first_name', 'last_name')
        else:
            # Perfil no es Administrador
            if not self.request.user.groups.filter(name__in=['Administrador']).exists():
                if negocio is None:
                    queryset = User.objects.filter(
                        negocio__in=self.request.user.negocio.all()).exclude(
                        groups__name__in=['Administrador']).order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')
                else:
                    # No es administrador y hay negocios seleccionadas
                    queryset = User.objects.filter(
                        negocio__in=negocio).exclude(
                        groups__name__in=['Administrador']).order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')

            else:
                # Es administrador y no hay negocio seleccionada.
                if negocio is None:
                    queryset = super(clienteView, self).get_queryset().order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')
                else:
                    # Es administrador y hay negocios seleccionadas.
                    queryset = super(clienteView, self).get_queryset().filter(
                        negocio__in=negocio).order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')

        return queryset


@login_required
@permission_required('users.add_user', raise_exception=True)
def create_cliente(request):
    if request.method == 'POST':

        cliente_form = CrearClienteForm(data=request.POST, user=request.user)
        print(request.POST)

        if cliente_form.is_valid():
            cliente = cliente_form.save(commit=False)
            cliente.status = True
            cliente.save()
            cliente = cliente_form.save()
            messages.success(request, 'Cliente Creado Exitosamente')
            return redirect('utils:create_cliente', cliente_id=cliente.id)
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        cliente_form = CrearClienteForm(user=request.user)
    
    return render(request, 'utils/cliente_create.html', {
        'form': cliente_form,
    })

class ClienteIdView(TemplateView):
    template_name = 'utils/create_cliente.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, cliente_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                print(cliente_id)
                data = []
                for i in Negocio.objects.filter(cliente=cliente_id, status=True):
                    data.append(i.toJSON())
            elif action == 'negocio_add':
                negocio = Negocio()
                negocio.nombre = request.POST['nombre']
                negocio.descripcion = request.POST['descripcion']
                negocio.archivo = request.FILES['archivo']
                negocio.cliente_id = cliente_id
                negocio.save()
            elif action == 'negocio_edit':
                negocio = Negocio.objects.get(pk=request.POST['id'])
                negocio.nombre = request.POST['nombre']
                negocio.descripcion = request.POST['descripcion']
                negocio.archivo = request.FILES['archivo']
                negocio.cliente_id = cliente_id
                negocio.save()
            elif action == 'contacto_delete':
                negocio = Negocio.objects.get(pk=request.POST['id'])
                negocio.status = False
                negocio.save()
            elif action == 'planta_add':
                bono = request.POST.getlist('bono')
                planta = Planta.objects.create(
                    negocio_id = request.POST['negocio'],
                    rut = request.POST['rut'],
                    nombre = request.POST['nombre'],
                    telefono = request.POST['telefono'],
                    email = request.POST['email'],
                    region_id = request.POST['region'],
                    provincia_id = request.POST['provincia'],
                    ciudad_id = request.POST['ciudad'],
                    direccion = request.POST['direccion'],
                    nombre_gerente = request.POST['nombre_gerente'],
                    rut_gerente = request.POST['rut_gerente'],
                    direccion_gerente = request.POST['direccion_gerente'],
                    gratificacion_id = request.POST['gratificacion'],
                    cliente_id = cliente_id                )

                for i in bono:
                    planta.bono.add(i)

    #         elif action == 'profesion_edit':
    #             profes = ProfesionUser.objects.get(pk=request.POST['id'])
    #             profes.egreso = request.POST['egreso']
    #             profes.institucion = request.POST['institucion']
    #             profes.profesion_id = request.POST['profesion']
    #             profes.user_id = user_id
    #             profes.save()
    #         elif action == 'profesion_delete':
    #             profes = ProfesionUser.objects.get(pk=request.POST['id'])
    #             profes.status = False
    #             profes.save()
    #         elif action == 'archivo_add':
    #             archiv = ArchivoUser()
    #             archiv.tipo_archivo_id = request.POST['tipo_archivo']
    #             archiv.url = request.POST['url']
    #             archiv.user_id = user_id
    #             archiv.save()
    #         elif action == 'archivo_edit':
    #             archiv = ArchivoUser.objects.get(pk=request.POST['id'])
    #             archiv.tipo_archivo_id = request.POST['tipo_archivo']
    #             archiv.url = request.POST['url']
    #             archiv.user_id = user_id
    #             archiv.save()
    #         elif action == 'archivo_delete':
    #             archiv = ArchivoUser.objects.get(pk=request.POST['id'])
    #             archiv.status = False
    #             archiv.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, cliente_id, **kwargs):
        cliente = get_object_or_404(Cliente, pk=cliente_id)

        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Contactos'
        context['list_url'] = reverse_lazy('users:<int:user_cliente>/create_cliente')
        context['entity'] = 'Contactos'
        context['cliente_id'] = cliente_id
        context['form1'] = CrearClienteForm(instance=cliente)
        context['form2'] = NegocioForm()
        context['form3'] = PlantaForm()
        return context


class NegocioView(TemplateView):
    """Profesion List
    Vista para listar todos los profesion según el usuario y sus las negocios
    relacionadas.
    """
    template_name = 'utils/create_cliente.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, cliente_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Negocio.objects.filter(cliente=cliente_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class PlantaView(TemplateView):
    """Profesion List
    Vista para listar todos los profesion según el usuario y sus las negocios
    relacionadas.
    """
    template_name = 'utils/create_cliente.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, cliente_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata2':
                data = []
                for i in Planta.objects.filter(cliente=cliente_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
