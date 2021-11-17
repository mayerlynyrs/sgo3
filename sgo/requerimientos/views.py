from django.shortcuts import render

# Create your views here.
"""Requerimientos  Views."""

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, ProtectedError
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
# Model
from requerimientos.models import Requerimiento
from utils.models import Negocio
# Form
from requerimientos.forms import RequerimientoCreateForm


class RequerimientoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Requerimiento List
    Vista para listar todos los requerimiento según el usuario y sus las negocios
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
        negocio = self.kwargs.get('negocio_id', None)

        if negocio == '':
            negocio = None

        if search:
            # Si el usuario no se administrador se despliegan los requerimientos en estado status
            # de las negocios a las que pertenece el usuario, según el critero de busqueda.
            if not self.request.user.groups.filter(name__in=['Administrador', ]).exists():
                queryset = super(RequerimientoListView, self).get_queryset().filter(
                    Q(status=True),
                    Q(negocios__in=self.request.user.negocio.all()),
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
            # status de las negocios a las que pertenece el usuario.
            if not self.request.user.groups.filter(name__in=['Administrador']).exists():
                queryset = super(RequerimientoListView, self).get_queryset().filter(
                    Q(status=True),
                    Q(negocios__in=self.request.user.negocio.all())
                ).distinct()
            else:
                # Si el usuario es administrador, se despliegan todos los requerimientos.
                if negocio is None:
                    queryset = super(RequerimientoListView, self).get_queryset()
                else:
                    # Si recibe la negocio, solo muestra los requerimientos que pertenecen a esa negocio.
                    queryset = super(RequerimientoListView, self).get_queryset().filter(
                        Q(negocios=negocio)
                    ).distinct()

        return queryset


class RequerimientoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Requerimiento Create
    Vista para crear un fichero digital.
    """

    def get_form_kwargs(self):
        kwargs = super(RequerimientoCreateView, self).get_form_kwargs()
        if self.request.POST:
            kwargs['user'] = self.request.user

        return kwargs

    form_class = RequerimientoCreateForm
    template_name = "ficheros/fichero_create.html"

    success_url = reverse_lazy('ficheros:list')
    success_message = 'Fichero Creado Exitosamente!'

    permission_required = 'ficheros.add_fichero'
    raise_exception = True


@login_required
@permission_required('ficheros.add_fichero', raise_exception=True)
def create_requerimiento(request):
    if request.method == 'POST':

        form = RequerimientoCreateForm(data=request.POST, files=request.FILES, user=request.user)

        if form.is_valid():
            requerimiento = form.save()

            messages.success(request, 'Fichero Creado Exitosamente')
            return redirect('ficheros:list')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = RequerimientoCreateForm(user=request.user)

    return render(request, 'ficheros/fichero_create.html', {
        'form': form,
    })


@login_required
@permission_required('ficheros.change_fichero', raise_exception=True)
def update_fichero(request, fichero_id):

    fichero = get_object_or_404(Requerimiento, pk=fichero_id)

    # Se obtienen las negocios del usuario.
    try:
        negocios_usuario = Negocio.objects.values_list('id', flat=True).filter(user=request.user)
    except:
        negocios_usuario = ''

    if request.method == 'POST':

        form = RequerimientoCreateForm(data=request.POST, instance=fichero, files=request.FILES, user=request.user)

        if form.is_valid():
            fichero = form.save()
            messages.success(request, 'Requerimiento Actualizado Exitosamente')
            page = request.GET.get('page')
            if page != '':
                response = redirect('ficheros:list')
                response['Location'] += '?page=' + page
                return response
            else:
                return redirect('ficheros:list')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = RequerimientoCreateForm(instance=fichero,
                                 initial={'negocios': list(negocios_usuario), },
                                 user=request.user)

    return render(
        request=request,
        template_name='ficheros/fichero_create.html',
        context={
            'fichero': fichero,
            'form': form
        })


@login_required
@permission_required('ficheros.view_fichero', raise_exception=True)
def detail_fichero(request, fichero_id, template_name='ficheros/partial_fichero_detail.html'):
    data = dict()
    fichero = get_object_or_404(Requerimiento, pk=fichero_id)

    context = {'fichero': fichero, }
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


@login_required
def delete_fichero(request, object_id, template_name='ficheros/fichero_delete.html'):
    data = dict()
    object = get_object_or_404(Requerimiento, pk=object_id)
    if request.method == 'POST':
        try:
            object.delete()
            messages.success(request, 'Fichero eliminado Exitosamente')
        except ProtectedError:
            messages.error(request, 'Fichero no se pudo Eliminar.')
            return redirect('ficheros:update', object_id)

        return redirect('ficheros:list')

    context = {'object': object}
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request
    )
    return JsonResponse(data)
