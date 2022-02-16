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
from utils.forms import AreaForm, CargoForm, HorarioForm, BonoForm, CrearClienteForm, EditarClienteForm, NegocioForm, PlantaForm, SaludForm, AfpForm, ValoresDiarioForm, ValoresDiarioAfpForm


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count
# Modelo
from utils.models import Area, Cargo, Horario, Bono, Negocio, Planta, Cliente, Region
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
                cargo.alias = request.POST['alias']
                cargo.descripcion = request.POST['descripcion']
                cargo.nombre_alias = request.POST['nombre']+request.POST['alias']
                cargo.status = True
                # espec.created_date = request.POST['created_date']
                cargo.save()
            elif action == 'edit':
                cargo = Cargo.objects.get(pk=request.POST['id'])
                cargo.nombre = request.POST['nombre']
                cargo.alias = request.POST['alias']
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


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Planta
    template_name = "utils/clientes_list.html"
    paginate_by = 25
    ordering = ['negocio', 'cliente']

    permission_required = 'utils.view_client'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)

        if self.request.user.groups.filter(name__in=['Administrador']).exists():
            institutions = Negocio.objects.values(
                    value=F('id'),
                    title=F('nombre')).all().order_by('nombre')
                #cache.set('institutions', institutions)
            institutions = Cliente.objects.values(
                    value=F('id'),
                    title=F('razon_social')).all().order_by('razon_social')

            context['negocios'] = institutions
            context['negocio'] = self.kwargs.get('negocio_id', None)
            negocios = Negocio.objects.filter(cliente=1)
            clientes = Cliente.objects.all()
            context['clients'] = Cliente.objects.all()
            # context['clients'] = Cliente.objects.filter(
            #     status=True).order_by(
            #         'razon_social').distinct('razon_social')
            context['business'] = Negocio.objects.filter(
                cliente__negocio__in=negocios).order_by('id', 'nombre').distinct('id', 'nombre')
            # context['business'] = Negocio.objects.filter(
            #     status=True).order_by('id', 'nombre').distinct('id', 'nombre')

            ######## MAYE ########
            context['consulta'] = Cliente.objects.raw('SELECT p.nombre as plantas, n.nombre, c.razon_social, c.id FROM utils_planta p FULL JOIN utils_negocio n ON p.negocio_id= n.id FULL JOIN utils_cliente c ON c.id = n.cliente_id')
            # Cliente.objects.all().order_by('cliente', 'negocio')
            # Planta.objects.filter(cliente__negocio__in=negocios).order_by('id', 'nombre').distinct('id', 'nombre')
            # Cliente.objects.all().select_related('planta').values_list('id', 'planta__negocio')

        return context

    def get_queryset(self):
        search = self.request.GET.get('q')
        negocio = self.kwargs.get('negocio_id', None)

        if negocio == '':
            negocio = None

        if search:
            # No es administrador y recibe parametro de busqueda
            if not self.request.user.groups.filter(name__in=['Administrador', ]).exists():
                queryset = Planta.objects.select_related('negocio').filter(
                    Q(cliente__in=self.request.user.cliente.all()),
                    Q(negocio__in=self.request.user.negocio.all()),
                    Q(planta__in=self.request.user.planta.all()),
                    Q(nombre__icontains=search) |
                    Q(telefono__icontains=search) |
                    Q(email__icontains=search)).exclude(
                    groups__name__in=['Administrador']).order_by(
                    'nombre', 'telefono').distinct('nombre', 'telefono')
            else:
                # Es administrador y recibe parametro de busqueda
                queryset = super(ClientListView, self).get_queryset().filter(
                                        Q(nombre__icontains=search) |
                                        Q(telefono__icontains=search) |
                                        Q(rut__icontains=search) |
                                        Q(groups__name__icontains=search) |
                                        Q(email__icontains=search)).order_by(
                    'nombre', 'telefono').distinct('nombre', 'telefono')
        else:
            # Perfil no es Administrador
            if not self.request.user.groups.filter(name__in=['Administrador']).exists():
                if negocio is None:
                    queryset = Planta.objects.filter(
                        negocio__in=self.request.user.negocio.all()).exclude(
                        groups__name__in=['Administrador']).order_by(
                        'nombre', 'telefono').distinct('nombre', 'telefono')
                else:
                    # No es administrador y hay negocios seleccionadas
                    queryset = Planta.objects.filter(
                        negocio__in=negocio).exclude(
                        groups__name__in=['Administrador']).order_by(
                        'nombre', 'telefono').distinct('nombre', 'telefono')

            else:
                # Es administrador y no hay negocio seleccionada.
                if negocio is None:
                    queryset = super(ClientListView, self).get_queryset().order_by(
                        'nombre', 'telefono').distinct('nombre', 'telefono')
                else:
                    # Es administrador y hay negocios seleccionadas.
                    queryset = super(ClientListView, self).get_queryset().filter(
                        negocio__in=negocio).order_by(
                        'nombre', 'telefono').distinct('nombre', 'telefono')

        return queryset


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


@login_required(login_url='users:signin')
def update_cliente(request, cliente_id):
    """Update a cliente's profile view."""
    print('aqui update_cliente')

    cliente = get_object_or_404(Cliente, pk=cliente_id)

    # Se valida que solo el administrador  pueda editar el perfil de otro usuario.
    # Se valida que solo los administradores puedan editar el perfil de otro usuario.
    if not request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
        if not cliente == request.user:
            raise Http404

    # Se obtiene el perfil y las negocios del usuario.
    try:
        current_group = cliente.groups.get()
        negocios_usuario = Negocio.objects.values_list('id', flat=True).filter(user=cliente_id)
        #negocios_usuario[::1]
    except:
        current_group = ''
        negocios_usuario = ''

    if request.method == 'POST':
        cliente_form = EditarClienteForm(request.POST or None, instance=cliente, user=request.user)
        #profile_form = ProfileForm(request.POST or None, request.FILES, instance=profile)

        if cliente_form.is_valid():
            cliente.is_active = True
            cliente_form.save()
            #profile_form.save()

            # Solo el Administrador puede cambiar el perfil del usuario
            if request.user.groups.filter(name__in=['Administrador', ]).exists():
                print('cliente.groups.clear()')
                # user.groups.clear()
                # user.groups.add(cliente_form.cleaned_data['group'])

            messages.success(request, ('Cliente actualizado'))

            if request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
                page = request.GET.get('page')
                if page != '':
                    response = redirect('utils:create_cliente', cliente_id)
                    # response['Location'] += '?page=' + page
                    return response
                else:
                    return redirect('utils:create_cliente', cliente_id)

            # if request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
            #     page = request.GET.get('page')
            #     if page != '':
            #         response = redirect('users:create', user_id)
            #         return response
            #     else:
            #         return redirect('users:create', user_id)
            else:
                return redirect('home')

        else:
            messages.error(request, ('Revisa el formulario e intentalo de nuevo.'))
    else:

        cliente_form = EditarClienteForm(
            instance=cliente,
            initial={'group': current_group.pk, 'negocio': list(negocios_usuario), },
            user=request.user
        )
        #profile_form = ProfileForm(instance=profile)

    return render(
        request=request,
        template_name='utils/create_cliente.html',
        context={
            'cliente': cliente,
            'form1': cliente_form
        }
    )


class ClienteIdView(TemplateView):
    template_name = 'utils/create_cliente.html'
    cliente_id=Cliente
    
    cliente = get_object_or_404(Cliente, pk=1)

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
                for i in Cliente.objects.filter(id=cliente_id, status=True):
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
            elif action == 'negocio_delete':
                negocio = Negocio.objects.get(pk=request.POST['id'])
                negocio.status = False
                negocio.save()
            elif action == 'planta_add':
                bono = request.POST.getlist('bono')
                examen = request.POST.getlist('examen')
                planta = Planta()
                planta.negocio_id = request.POST['negocio']
                planta.rut = request.POST['rut']
                planta.nombre = request.POST['nombre']
                planta.telefono = request.POST['telefono']
                planta.email = request.POST['email']
                planta.region_id = request.POST['region']
                planta.provincia_id = request.POST['provincia']
                planta.ciudad_id = request.POST['ciudad']
                planta.direccion = request.POST['direccion']
                planta.nombre_gerente = request.POST['nombre_gerente']
                planta.rut_gerente = request.POST['rut_gerente']
                planta.direccion_gerente = request.POST['direccion_gerente']
                planta.gratificacion_id = request.POST['gratificacion']
                planta.cliente_id = cliente_id
                planta.save()
                for i in bono:
                    planta.bono.add(i)
                for e in examen:
                    planta.examen.add(e)
            elif action == 'planta_edit':
                bono = request.POST.getlist('bono')
                examen = request.POST.getlist('examen')
                planta = Planta.objects.get(pk=request.POST['id'])
                planta.negocio_id = request.POST['negocio']
                planta.rut = request.POST['rut']
                planta.nombre = request.POST['nombre']
                planta.telefono = request.POST['telefono']
                planta.email = request.POST['email']
                planta.region_id = request.POST['region']
                planta.provincia_id = request.POST['provincia']
                planta.ciudad_id = request.POST['ciudad']
                planta.direccion = request.POST['direccion']
                planta.nombre_gerente = request.POST['nombre_gerente']
                planta.rut_gerente = request.POST['rut_gerente']
                planta.direccion_gerente = request.POST['direccion_gerente']
                planta.gratificacion_id = request.POST['gratificacion']
                planta.cliente_id = cliente_id
                planta.save()
                for i in bono:
                    planta.bono.add(i)
                for e in examen:
                    planta.examen.add(e)
                    
            elif action == 'planta_delete':
                archiv = Planta.objects.get(pk=request.POST['id'])
                archiv.status = False
                archiv.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(request, cliente_id, **kwargs):

        cliente = get_object_or_404(Cliente, pk=cliente_id)

        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Contactos'
        context['list_url'] = reverse_lazy('users:<int:user_cliente>/create_cliente')
        context['update_url'] = reverse_lazy('utils:update_cliente')
        context['cliente'] = cliente
        context['entity'] = 'Contactos'
        context['cliente_id'] = cliente_id
        context['form1'] = CrearClienteForm(instance=cliente)
        context['form2'] = NegocioForm()
        context['form3'] = PlantaForm(instance=cliente, cliente_id=cliente_id)
        # context['form3'] = PlantaForm(instance=cliente, cliente=request.cliente)
        return context


class NegocioView(TemplateView):
    """Negocio List
    Vista para listar todos los negocios según el usuario y sus las negocios
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
    """Planta List
    Vista para listar todos las plantas según el usuario y sus las negocios
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
                salud.nombre = request.POST['nombre']
                salud.status = True
                # espec.created_date = request.POST['created_date']
                salud.save()
            elif action == 'edit':
                salud = Salud.objects.get(pk=request.POST['id'])
                salud.nombre = request.POST['nombre']
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
                previs.nombre = request.POST['nombre']
                previs.tasa = request.POST['tasa']
                previs.status = True
                # espec.created_date = request.POST['created_date']
                previs.save()
            elif action == 'edit':
                previs = Afp.objects.get(pk=request.POST['id'])
                previs.nombre = request.POST['nombre']
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
