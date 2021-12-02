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
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
# Forms
from users.forms import CrearUsuarioForm, ProfesionCreateForm


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from django.db.models import Count
# Modelo
from utils.models import Negocio
from ficheros.models import Fichero
from contratos.models import Contrato
from users.models import User, Profesion


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


class ProfesionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Profesion List
    Vista para listar todos los profesion según el usuario y sus las negocios
    relacionadas.
    """
    model = Profesion
    template_name = "profesiones/profesion_list.html"
    paginate_by = 25
    ordering = ['created_date', ]

    permission_required = 'profesiones.view_profesion'
    raise_exception = True

    def get_queryset(self):
        search = self.request.GET.get('q')
        negocio = self.kwargs.get('negocio_id', None)

        if negocio == '':
            negocio = None

        if search:
            # Si el usuario no se administrador se despliegan los profesiones en estado status
            # de las negocios a las que pertenece el usuario, según el critero de busqueda.
            if not self.request.user.groups.filter(name__in=['Administrador', ]).exists():
                queryset = super(ProfesionListView, self).get_queryset().filter(
                    Q(status=True),
                    Q(nombre__icontains=search)
                ).distinct()
            else:
                # Si el usuario es administrador se despliegan todos los profesiones
                # segun el critero de busqueda.
                queryset = super(ProfesionListView, self).get_queryset().filter(
                    Q(nombre__icontains=search)
                ).distinct()
        else:
            # Si el usuario no es administrador, se despliegan los profesiones en estado
            # status de las negocios a las que pertenece el usuario.
            if not self.request.user.groups.filter(name__in=['Administrador']).exists():
                queryset = super(ProfesionListView, self).get_queryset().filter(
                    Q(status=True)
                ).distinct()
            else:
                # Si el usuario es administrador, se despliegan todos los profesiones.
                if negocio is None:
                    queryset = super(ProfesionListView, self).get_queryset()
                else:
                    # Si recibe la negocio, solo muestra los profesiones que pertenecen a esa negocio.
                    queryset = super(ProfesionListView, self).get_queryset().filter(
                        Q(negocios=negocio)
                    ).distinct()

        return queryset


class ProfesionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Profesion Create
    Vista para crear un profesion.
    """

    def get_form_kwargs(self):
        kwargs = super(ProfesionCreateView, self).get_form_kwargs()
        if self.request.POST:
            kwargs['user'] = self.request.user

        return kwargs

    form_class = ProfesionCreateForm
    template_name = "users/profesion_create.html"

    success_url = reverse_lazy('profesiones:list')
    success_message = 'Profesion Creado Exitosamente!'

    permission_required = 'profesiones.add_profesion'
    raise_exception = True


@login_required
@permission_required('profesiones.add_profesion', raise_exception=True)
def create_profesion(request):
    if request.method == 'POST':

        form = ProfesionCreateForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            profesion = form.save()

            messages.success(request, 'Profesion Creado Exitosamente')
            return redirect('utils:list_profesion')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = ProfesionCreateForm()

    return render(request, 'users/profesion_create.html', {
        'form': form,
    })


@login_required
@permission_required('profesiones.change_profesion', raise_exception=True)
def update_profesion(request, profesion_id):

    profesion = get_object_or_404(Profesion, pk=profesion_id)

    if request.method == 'POST':

        form = ProfesionCreateForm(data=request.POST, instance=profesion, files=request.FILES)

        if form.is_valid():
            profesion = form.save()
            messages.success(request, 'Profesion Actualizado Exitosamente')
            page = request.GET.get('page')
            if page != '':
                response = redirect('utils:list_profesion')
                response['Location'] += '?page=' + page
                return response
            else:
                return redirect('utils:list_profesion')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = ProfesionCreateForm(instance=profesion)

    return render(
        request=request,
        template_name='users/profesion_create.html',
        context={
            'profesion': profesion,
            'form': form
        })


@login_required
@permission_required('profesiones.view_profesion', raise_exception=True)
def detail_profesion(request, profesion_id, template_name='profesiones/partial_profesion_detail.html'):
    data = dict()
    profesion = get_object_or_404(Profesion, pk=profesion_id)

    context = {'profesion': profesion, }
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


@login_required
def delete_profesion(request, object_id, template_name='profesiones/profesion_delete.html'):
    data = dict()
    object = get_object_or_404(Profesion, pk=object_id)
    if request.method == 'POST':
        try:
            object.delete()
            messages.success(request, 'Profesion eliminado Exitosamente')
        except ProtectedError:
            messages.error(request, 'Profesion no se pudo Eliminar.')
            return redirect('profesiones:update', object_id)

        return redirect('profesiones:list')

    context = {'object': object}
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request
    )
    return JsonResponse(data)
