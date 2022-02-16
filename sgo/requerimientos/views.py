from django.shortcuts import render

# Create your views here.
"""Requerimientos  Views."""

# Django
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, ProtectedError
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
# Model
from requerimientos.models import Requerimiento, AreaCargo, RequerimientoUser
from utils.models import Negocio, Planta
# Form
from requerimientos.forms import RequerimientoCreateForm, ACRForm, RequeriUserForm


class RequerimientoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Requerimiento List
    Vista para listar todos los requerimiento según el usuario y sus las plantas
    relacionadas.
    """
    model = Requerimiento
    template_name = "requerimientos/requerimiento_list.html"
    paginate_by = 25
    ordering = ['modified', ]

    permission_required = 'requerimientos.view_requerimiento'
    raise_exception = True

    def get_queryset(self):
        search = self.request.GET.get('q')
        planta = self.kwargs.get('planta_id', None)

        if planta == '':
            planta = None

        if search:
            # Si el usuario no se administrador se despliegan los requerimientos en estado status
            # de las plantas a las que pertenece el usuario, según el critero de busqueda.
            if not self.request.user.groups.filter(name__in=['Administrador', ]).exists():
                queryset = super(RequerimientoListView, self).get_queryset().filter(
                    Q(status=True),
                    Q(plantas__in=self.request.user.planta.all()),
                    Q(nombre__icontains=search)
                ).distinct()
            else:
                # Si el usuario es administrador se despliegan todos los requerimientos
                # segun el critero de busqueda.
                queryset = super(RequerimientoListView, self).get_queryset().filter(
                    Q(nombre__icontains=search)
                ).distinct()
        else:
            # Si el usuario no es administrador, se despliegan los requerimientos en estado
            # status de las plantas a las que pertenece el usuario.
            if not self.request.user.groups.filter(name__in=['Administrador']).exists():
                queryset = super(RequerimientoListView, self).get_queryset().filter(
                    Q(status=True),
                    Q(plantas__in=self.request.user.planta.all())
                ).distinct()
            else:
                # Si el usuario es administrador, se despliegan todos los requerimientos.
                if planta is None:
                    queryset = super(RequerimientoListView, self).get_queryset()
                else:
                    # Si recibe la planta, solo muestra los requerimientos que pertenecen a esa planta.
                    queryset = super(RequerimientoListView, self).get_queryset().filter(
                        Q(plantas=planta)
                    ).distinct()

        return queryset


class RequerimientoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Requerimiento Create
    Vista para crear un requerimiento.
    """

    def get_form_kwargs(self):
        kwargs = super(RequerimientoCreateView, self).get_form_kwargs()
        if self.request.POST:
            kwargs['user'] = self.request.user

        return kwargs

    form_class = RequerimientoCreateForm
    template_name = "requerimientos/requerimiento_create.html"

    success_url = reverse_lazy('requerimientos:list')
    success_message = 'Requerimiento Creado Exitosamente!'

    permission_required = 'requerimientos.add_requerimiento'
    raise_exception = True


@login_required
@permission_required('requerimientos.add_requerimiento', raise_exception=True)
def create_requerimiento(request):
    if request.method == 'POST':

        requer_form = RequerimientoCreateForm(data=request.POST)
        # print(request.POST)

        if requer_form.is_valid():
            requerimiento = requer_form.save(commit=False)
            requerimiento.status = True
            requerimiento.codigo = requerimiento.id
            requerimiento.save()
            folio = Requerimiento.objects.filter(cliente__pk=requerimiento.cliente.id).count()
            code = requerimiento.cliente.abreviatura + str (folio)
            # code = requerimiento.cliente.abreviatura + str (requerimiento.id)
            requerimiento.codigo = code
            requerimiento = requer_form.save()

            messages.success(request, 'Requerimiento Creado Exitosamente')
            return redirect('requerimientos:create_requerimiento', requerimiento_id=requerimiento.id)
            # return redirect('utils:create_cliente', requerimiento_id=requerimiento.id)
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        requer_form = RequerimientoCreateForm()
    
    return render(request, 'requerimientos/requerimiento_create.html', {
        'form': requer_form,
    })



@login_required
@permission_required('requerimientos.change_requerimiento', raise_exception=True)
def update_requerimiento(request, requerimiento_id):

    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)

    # Se obtienen las plantas del usuario.
    try:
        plantas_usuario = Planta.objects.values_list('id', flat=True).filter(user=request.user)
    except:
        plantas_usuario = ''

    if request.method == 'POST':

        form = RequerimientoCreateForm(data=request.POST, instance=requerimiento, files=request.FILES, user=request.user)

        if form.is_valid():
            requerimiento = form.save()
            messages.success(request, 'Requerimiento Actualizado Exitosamente')
            page = request.GET.get('page')
            if page != '':
                response = redirect('requerimientos:list')
                response['Location'] += '?page=' + page
                return response
            else:
                return redirect('requerimientos:list')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = RequerimientoCreateForm(instance=requerimiento,
                                 initial={'plantas': list(plantas_usuario), },
                                 user=request.user)

    return render(
        request=request,
        template_name='requerimientos/requerimiento_create.html',
        context={
            'requerimiento': requerimiento,
            'form': form
        })


@login_required
@permission_required('requerimientos.view_requerimiento', raise_exception=True)
def detail_requerimiento(request, requerimiento_id, template_name='requerimientos/partial_requerimiento_detail.html'):
    data = dict()
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)

    context = {'requerimiento': requerimiento, }
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


@login_required
def delete_requerimiento(request, object_id, template_name='requerimientos/requerimiento_delete.html'):
    data = dict()
    object = get_object_or_404(Requerimiento, pk=object_id)
    if request.method == 'POST':
        try:
            object.delete()
            messages.success(request, 'Requerimiento eliminado Exitosamente')
        except ProtectedError:
            messages.error(request, 'Requerimiento no se pudo Eliminar.')
            return redirect('requerimientos:update', object_id)

        return redirect('requerimientos:list')

    context = {'object': object}
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request
    )
    return JsonResponse(data)

class RequerimientoIdView(TemplateView):
    template_name = 'requerimientos/create_requerimiento.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, requerimiento_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                print(requerimiento_id)
                data = []
                for i in Requerimiento.objects.filter(id=requerimiento_id, status=True):
                    data.append(i.toJSON())
            elif action == 'acr_add':
                negocio = AreaCargo()
                negocio.nombre = request.POST['nombre']
                negocio.descripcion = request.POST['descripcion']
                negocio.archivo = request.FILES['archivo']
                negocio.cliente_id = requerimiento_id
                negocio.save()
            elif action == 'acr_edit':
                negocio = AreaCargo.objects.get(pk=request.POST['id'])
                negocio.nombre = request.POST['nombre']
                negocio.descripcion = request.POST['descripcion']
                negocio.archivo = request.FILES['archivo']
                negocio.cliente_id = requerimiento_id
                negocio.save()
            elif action == 'acr_delete':
                negocio = AreaCargo.objects.get(pk=request.POST['id'])
                negocio.status = False
                negocio.save()
            elif action == 'requeri_user_add':
                bono = request.POST.getlist('bono')
                examen = request.POST.getlist('examen')
                planta = RequerimientoUser.objects.create(
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
                    cliente_id = requerimiento_id                )
                for i in bono:
                    planta.bono.add(i)
                for e in examen:
                    planta.examen.add(e)
            elif action == 'requeri_user_edit':

                bono = request.POST.getlist('bono')
                examen = request.POST.getlist('examen')
                planta = RequerimientoUser.objects.create(
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
                    cliente_id = requerimiento_id                )
                for i in bono:
                    planta.bono.add(i)
                for e in examen:
                    planta.examen.add(e)
                    
            elif action == 'requeri_user_delete':
                archiv = RequerimientoUser.objects.get(pk=request.POST['id'])
                archiv.status = False
                archiv.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, requerimiento_id, **kwargs):

        requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)

        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('users:<int:user_cliente>/create_cliente')
        context['update_url'] = reverse_lazy('requerimientos:update')
        context['entity'] = 'Requerimientos'
        context['requerimiento_id'] = requerimiento_id
        context['form'] = RequerimientoCreateForm(instance=requerimiento)
        context['form2'] = ACRForm(instance=requerimiento)
        context['form3'] = RequeriUserForm(instance=requerimiento)
        return context


class ACRView(TemplateView):
    """Areas y Cargos del Requerimiento List
    Vista para listar todos los AreaCargo según el Requerimiento
    relacionado.
    """
    template_name = 'requerimientos/create_requerimiento.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, requerimiento_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata2':
                data = []
                for i in AreaCargo.objects.filter(requerimiento=requerimiento_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class RequirementUserView(TemplateView):
    """RequirementUser List
    Vista para listar todos los requirementos del usuario y sus las negocios
    relacionadas.
    """
    template_name = 'requerimientos/create_requerimiento.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, area_cargo_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata3':
                data = []
                for i in RequerimientoUser.objects.filter(area_cargo=area_cargo_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
