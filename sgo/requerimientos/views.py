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

# Planta
def load_plantas(request):
    cliente_id = request.GET.get('cliente')    
    plantas = Planta.objects.filter(cliente_id=cliente_id).order_by('nombre')
    context = {'plantas': plantas}
    return render(request, 'requerimientos/planta.html', context)


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

        form = RequerimientoCreateForm(request.POST or None, instance=requerimiento)

        if form.is_valid():
            requerimiento = form.save()
            messages.success(request, 'Requerimiento Actualizado Exitosamente')
            page = request.GET.get('page')
            if page != '':
                response = redirect('requerimientos:create_requerimiento', requerimiento_id)
                # response['Location'] += '?page=' + str(page)
                return response
            else:
                return redirect('requerimientos:create_requerimiento', requerimiento_id)
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
                ac_r = AreaCargo()
                ac_r.cantidad = request.POST['cantidad']
                ac_r.valor_aprox = request.POST['valor_aprox']
                ac_r.fecha_ingreso = request.POST['fecha_ingreso']
                ac_r.area_id = request.POST['area']
                ac_r.cargo_id = request.POST['cargo']
                ac_r.requerimiento_id = requerimiento_id
                ac_r.save()
            elif action == 'acr_edit':
                ac_r = AreaCargo.objects.get(pk=request.POST['id'])
                ac_r.cantidad = request.POST['cantidad']
                ac_r.valor_aprox = request.POST['valor_aprox']
                ac_r.fecha_ingreso = request.POST['fecha_ingreso']
                ac_r.area_id = request.POST['area']
                ac_r.cargo_id = request.POST['cargo']
                ac_r.requerimiento_id = requerimiento_id
                ac_r.save()
            elif action == 'acr_delete':
                ac_r = AreaCargo.objects.get(pk=request.POST['id'])
                ac_r.status = False
                ac_r.save()
            elif action == 'requeri_user_add':
                trabaj = RequerimientoUser()
                if "referido" in request.POST:
                    estado = True
                    trabaj.referido =  estado
                else:
                    estado = False
                    trabaj.referido =  estado
                trabaj.descripcion = request.POST['descripcion']
                trabaj.tipo_id = request.POST['tipo']
                trabaj.pension = request.POST['pension']
                trabaj.user_id = request.POST['user']
                trabaj.jefe_area_id = request.POST['jefe_area']
                trabaj.area_cargo_id = 10
                trabaj.requerimiento_id = requerimiento_id
                trabaj.save()
            elif action == 'requeri_user_edit':
                trabaj = RequerimientoUser.objects.get(pk=request.POST['id'])
                if "referido" in request.POST:
                    estado = True
                    trabaj.referido =  estado
                else:
                    estado = False
                    trabaj.referido =  estado
                trabaj.descripcion = request.POST['descripcion']
                trabaj.tipo_id = request.POST['tipo']
                trabaj.pension = request.POST['pension']
                trabaj.user_id = request.POST['user']
                trabaj.jefe_area_id = request.POST['jefe_area']
                trabaj.area_cargo_id = 10
                trabaj.requerimiento_id = requerimiento_id
                trabaj.save()
            elif action == 'requeri_user_delete':
                trabaj = RequerimientoUser.objects.get(pk=request.POST['id'])
                trabaj.status = False
                trabaj.save()
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
        context['form2'] = ACRForm(instance=requerimiento,
                                   areas=requerimiento.cliente.area.all(),
                                   cargos=requerimiento.cliente.cargo.all()
                                   )
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

    def post(self, request, requerimiento_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata3':
                data = []
                # for i in RequerimientoUser.objects.filter(area_cargo=area_cargo_id, status=True):
                for i in RequerimientoUser.objects.filter(requerimiento=requerimiento_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
