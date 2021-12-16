"""Users views."""

import json
# Django
import os
from subprocess import Popen
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, F, ProtectedError
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from mailmerge import MailMerge
from django.conf import settings
# Models
from users.models import Sexo, Profesion, ProfesionUser
from utils.models import Cliente, Negocio, Region, Provincia, Ciudad
from contratos.models import Plantilla, Contrato, DocumentosContrato
# Forms
from users.forms import EditarAtributosForm, EditarUsuarioForm, CrearUsuarioForm, ProfesionCreateForm, ProfesionUserCreateForm, ParentescoCreateForm, ContactoCreateForm, ArchivoUserCreateForm, TipoArchivoCreateForm

User = get_user_model()


# Región/Provincia/Ciudad
def load_provincias(request):
    region_id = request.GET.get('region')    
    provincias = Provincia.objects.filter(region_id=region_id).order_by('nombre')
    context = {'provincias': provincias}
    return render(request, 'users/provincia.html', context)

def load_ciudades(request):
    provincia_id = request.GET.get('provincia')    
    ciudades = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
    context = {'ciudades': ciudades}
    return render(request, 'users/ciudad.html', context)

# Negocio
def load_negocios(request):
    cliente_id = request.GET.get('cliente')    
    negocios = Negocio.objects.filter(cliente_id=cliente_id).order_by('nombre')
    context = {'negocios': negocios}
    return render(request, 'users/negocio.html', context)


class SignInView(auth_views.LoginView):
    """Login view."""

    template_name = 'users/login.html'


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = "users/users_list.html"
    paginate_by = 25
    ordering = ['first_name', 'last_name']

    permission_required = 'users.view_user'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

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
                queryset = super(UserListView, self).get_queryset().filter(
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
                    queryset = super(UserListView, self).get_queryset().order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')
                else:
                    # Es administrador y hay negocios seleccionadas.
                    queryset = super(UserListView, self).get_queryset().filter(
                        negocio__in=negocio).order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')

        return queryset


@login_required
@permission_required('users.add_user', raise_exception=True)
def create_user(request):
    if request.method == 'POST':

        user_form = CrearUsuarioForm(data=request.POST, user=request.user)
        #profile_form = ProfileForm(data=request.POST, user=request.user)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            # print(request.POST.getlist('group'))
            if request.POST.getlist('group') == ['1']:
                user.is_superuser = True
                user.is_staff = True
                user.atributos = 'NO APLICA'
            # exit()
            email = user.email
            now_date = datetime.now()
            user.username = email[:email.find('@')] + now_date.strftime("-%y%m%H%M%S")
            user.set_password(user.first_name[0:2].lower()+user.last_name[0:2].lower()+user.rut[0:4])
            user.is_active = True
            user.save()
            user = user_form.save()

            #profile = profile_form.save(commit=False)

            user.groups.add(user_form.cleaned_data['group'])

            # current_site = str(get_current_site(request))
            #
            # # task para enviar mail de activacion
            # send_activation_mail.apply_async(
            #     queue='high_priority',
            #     kwargs={'current_site': current_site,
            #             'user_id': user.pk
            #             }
            # )

            messages.success(request, 'Usuario Creado Exitosamente')
            return redirect('users:create', user_id=user.id)
            # return redirect('users:list')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        user_form = CrearUsuarioForm(user=request.user)
        #profile_form = ProfileForm(initial={'institution': institution}, user=request.user)
    
    return render(request, 'users/users_create.html', {
        'form': user_form,
    })


@login_required
@permission_required('users.add_user', raise_exception=True)
def users_create(request, user_id):

    user = get_object_or_404(User, pk=user_id)

    # Se valida que solo el administrador  pueda editar el perfil de otro usuario.
    # Se valida que solo los administradores puedan editar el perfil de otro usuario.
    if not request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
        if not user == request.user:
            raise Http404

    # Se obtiene el perfil y las negocios del usuario.
    try:
        current_group = user.groups.get()
        negocios_usuario = Negocio.objects.values_list('id', flat=True).filter(user=user_id)
        #negocios_usuario[::1]
    except:
        current_group = ''
        negocios_usuario = ''

    if request.method == 'POST':
        user_form = EditarUsuarioForm(request.POST or None, instance=user, user=request.user)
        #profile_form = ProfileForm(request.POST or None, request.FILES, instance=profile)

        if user_form.is_valid():
            user_form.save()
            #profile_form.save()

            # Solo el Administrador puede cambiar el perfil del usuario
            if request.user.groups.filter(name__in=['Administrador', ]).exists():
                user.groups.clear()
                user.groups.add(user_form.cleaned_data['group'])

            messages.success(request, ('Usuario actualizado'))

            if request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
                page = request.GET.get('page')
                if page != '':
                    response = redirect('users:detail', pk=user_id)
                    response['Location'] += '?page=' + page
                    return response
                else:
                    return redirect('users:detail', pk=user_id)
            else:
                return redirect('home')

        else:
            messages.error(request, ('Revisa el formulario e intentalo de nuevo.'))
    else:

        user_form = EditarUsuarioForm(
            instance=user,
            initial={'group': current_group.pk, 'negocio': list(negocios_usuario), },
            user=request.user
        )
        #profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':

        contacto_user_form = ContactoCreateForm(data=request.POST)
        
        if contacto_user_form.is_valid():
            contacto = contacto_user_form.save(commit=False)
            contacto.status = True
            now_date = datetime.now()
            contacto.created_date = now_date
            contacto.user_id = user_id
            print("2do-", user_id)
            contacto.save()
            contacto = contacto_user_form.save()
            

            messages.success(request, 'Contacto Usuario Creado Exitosamente')
            # return redirect('users:add_contacto', user_id=profesion_user.id)
            # return redirect('users:list')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')

        profesion_user_form = ProfesionUserCreateForm(data=request.POST)
        print("3ero-", user_id)

        if profesion_user_form.is_valid():
            profesion_user = profesion_user_form.save(commit=False)
            profesion_user.status = True
            now_date = datetime.now()
            profesion_user.created_date = now_date
            profesion_user.user_id = user_id
            print("4to-", user_id)
            profesion_user.save()
            profesion_user = profesion_user_form.save()
            

            messages.success(request, 'Profesion Usuario Creado Exitosamente')
            # return redirect('users:add_contacto', user_id=user_id)
            # return redirect('users:list')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')

        doc_user_form = ArchivoUserCreateForm(data=request.POST)
        print("5to-", user_id)

        if doc_user_form.is_valid():
            archivo_user = doc_user_form.save(commit=False)
            archivo_user.status = True
            now_date = datetime.now()
            archivo_user.created_date = now_date
            archivo_user.user_id = user_id
            print("6to-", user_id)
            archivo_user.save()
            archivo_user = doc_user_form.save()
            

            messages.success(request, 'Archivos del Usuario Creado Exitosamente')
            # return redirect('users:add_contacto', user_id=user_id)
            # return redirect('users:list')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        contacto_user_form = ContactoCreateForm(user=request.user)
        profesion_user_form = ProfesionUserCreateForm(user=request.user)
        doc_user_form = ArchivoUserCreateForm(user=request.user)
        #profile_form = ProfileForm(initial={'institution': institution}, user=request.user)

    
    return render(request, 'users/create_users.html', {
        'form2': contacto_user_form,
        'form3': profesion_user_form,
        'form4': doc_user_form,
        'form': user_form
    })

    # return render(
    #     request=request,
    #     template_name='users/users_create.html',
    #     context={
    #         'usuario': user,
    #         'form': user_form
    #     }
    # )
    
    # return render(request, 'users/users_create.html', {
    #     'form2': contacto_user_form,
    # })
    
    # return render(request, 'users/users_create.html', {
    #     'form1': user_form,
    # })


@login_required(login_url='users:signin')
def update_user(request, user_id):
    """Update a user's profile view."""

    user = get_object_or_404(User, pk=user_id)

    # Se valida que solo el administrador  pueda editar el perfil de otro usuario.
    # Se valida que solo los administradores puedan editar el perfil de otro usuario.
    if not request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
        if not user == request.user:
            raise Http404

    # Se obtiene el perfil y las negocios del usuario.
    try:
        current_group = user.groups.get()
        negocios_usuario = Negocio.objects.values_list('id', flat=True).filter(user=user_id)
        #negocios_usuario[::1]
    except:
        current_group = ''
        negocios_usuario = ''

    if request.method == 'POST':
        user_form = EditarUsuarioForm(request.POST or None, instance=user, user=request.user)
        #profile_form = ProfileForm(request.POST or None, request.FILES, instance=profile)

        if user_form.is_valid():
            user_form.save()
            #profile_form.save()

            # Solo el Administrador puede cambiar el perfil del usuario
            if request.user.groups.filter(name__in=['Administrador', ]).exists():
                user.groups.clear()
                user.groups.add(user_form.cleaned_data['group'])

            messages.success(request, ('Usuario actualizado'))

            if request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
                page = request.GET.get('page')
                if page != '':
                    response = redirect('users:detail', pk=user_id)
                    response['Location'] += '?page=' + page
                    return response
                else:
                    return redirect('users:detail', pk=user_id)
            else:
                return redirect('home')

        else:
            messages.error(request, ('Revisa el formulario e intentalo de nuevo.'))
    else:

        user_form = EditarUsuarioForm(
            instance=user,
            initial={'group': current_group.pk, 'negocio': list(negocios_usuario), },
            user=request.user
        )
        #profile_form = ProfileForm(instance=profile)

    return render(
        request=request,
        template_name='users/users_create.html',
        context={
            'usuario': user,
            'form': user_form
        }
    )


@login_required(login_url='users:signin')
def update_a_user(request, user_id):
    """Update a user's profile view (attributes)."""

    user = get_object_or_404(User, pk=user_id)

    # Se valida que solo el administrador  pueda editar el perfil de otro usuario.
    # Se valida que solo los administradores puedan editar el perfil de otro usuario.
    if not request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
        if not user == request.user:
            raise Http404

    if request.method == 'POST':
        user_form = EditarAtributosForm(request.POST or None, instance=user, user=request.user)
        #profile_form = ProfileForm(request.POST or None, request.FILES, instance=profile)

        if user_form.is_valid():
            user_form.save()
            #profile_form.save()

            messages.success(request, ('Usuario actualizado'))

            return redirect('users:attribute', user_id)

        else:
            messages.error(request, ('Revisa el formulario e intentalo de nuevo.'))
    else:

        user_form = EditarAtributosForm(
            instance=user,
            user=request.user
        )
        #profile_form = ProfileForm(instance=profile)

    # Obtengo todos los documentos del contrato
    contratos = Contrato.objects.filter(user=user)

    return render(
        request=request,
        template_name='users/users_attribute.html',
        context={
            'usuario': user,
            'form': user_form,
            'contratos': contratos
        }
    )


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/users_detail.html"
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)

        # Se valida que solo el administrador pueda editar el perfil de otro usuario.
        if not self.request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT',]).exists():
            if not self.object == self.request.user:
                raise Http404

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
    template_name = "profesiones/profesion_create.html"

    success_url = reverse_lazy('profesiones:list')
    success_message = 'Profesion Creado Exitosamente!'

    permission_required = 'profesiones.add_profesion'
    raise_exception = True


@login_required
@permission_required('profesiones.add_profesion', raise_exception=True)
def create_profesion(request, template_name='users/agregar_create.html'):
    if request.method == 'POST':
        form = ProfesionCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            profesion = form.save()
            messages.success(request, 'Profesion Creado Exitosamente')
            return redirect('users:list_profesion')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = ProfesionCreateForm()
        
        data = dict()

        context = {'form': form, }
        data['html_form'] = render_to_string(
                            template_name,
                            context,
                            request=request,
                        )
    return JsonResponse(data)


@login_required
@permission_required('profesiones.change_profesion', raise_exception=True)
def update_profesion(request, profesion_id):

    profesion = get_object_or_404(Profesion, pk=profesion_id)

    # Se obtienen las negocios del usuario.
    try:
        negocios_usuario = Negocio.objects.values_list('id', flat=True).filter(user=request.user)
    except:
        negocios_usuario = ''

    if request.method == 'POST':

        form = ProfesionCreateForm(data=request.POST, instance=profesion, files=request.FILES, user=request.user)

        if form.is_valid():
            profesion = form.save()
            messages.success(request, 'Profesion Actualizado Exitosamente')
            page = request.GET.get('page')
            if page != '':
                response = redirect('profesiones:list')
                response['Location'] += '?page=' + page
                return response
            else:
                return redirect('profesiones:list')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = ProfesionCreateForm(instance=profesion,
                                 initial={'negocios': list(negocios_usuario), },
                                 user=request.user)

    return render(
        request=request,
        template_name='profesiones/profesion_create.html',
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


class ProfesionUserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ProfesionUser
    template_name = "users/users_list.html"
    paginate_by = 25
    ordering = ['first_name', 'last_name']

    permission_required = 'users.view_user'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

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
                queryset = super(UserListView, self).get_queryset().filter(
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
                    queryset = super(UserListView, self).get_queryset().order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')
                else:
                    # Es administrador y hay negocios seleccionadas.
                    queryset = super(UserListView, self).get_queryset().filter(
                        negocio__in=negocio).order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')

        return queryset


@login_required(login_url='users:signin')
def update_profesion_user(request, user_id):
    """Update a user's profession view."""

    user = get_object_or_404(User, pk=user_id)

    # Se valida que solo el administrador  pueda editar el perfil de otro usuario.
    # Se valida que solo los administradores puedan editar el perfil de otro usuario.
    if not request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
        if not user == request.user:
            raise Http404

    # Se obtiene el perfil y las negocios del usuario.
    try:
        current_group = user.groups.get()
        negocios_usuario = Negocio.objects.values_list('id', flat=True).filter(user=user_id)
        #negocios_usuario[::1]
    except:
        current_group = ''
        negocios_usuario = ''

    if request.method == 'POST':
        user_form = EditarUsuarioForm(request.POST or None, instance=user, user=request.user)
        #profile_form = ProfileForm(request.POST or None, request.FILES, instance=profile)

        if user_form.is_valid():
            user_form.save()
            #profile_form.save()

            # Solo el Administrador puede cambiar el perfil del usuario
            if request.user.groups.filter(name__in=['Administrador', ]).exists():
                user.groups.clear()
                user.groups.add(user_form.cleaned_data['group'])

            messages.success(request, ('Usuario actualizado'))

            if request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
                page = request.GET.get('page')
                if page != '':
                    response = redirect('users:detail', pk=user_id)
                    response['Location'] += '?page=' + page
                    return response
                else:
                    return redirect('users:detail', pk=user_id)
            else:
                return redirect('home')

        else:
            messages.error(request, ('Revisa el formulario e intentalo de nuevo.'))
    else:

        user_form = EditarUsuarioForm(
            instance=user,
            initial={'group': current_group.pk, 'negocio': list(negocios_usuario), },
            user=request.user
        )
        #profile_form = ProfileForm(instance=profile)

    return render(
        request=request,
        template_name='users/users_create.html',
        context={
            'usuario': user,
            'form': user_form
        }
    )


@login_required(login_url='users:signin')
def update_a_user(request, user_id):
    """Update a user's profile view (attributes)."""

    user = get_object_or_404(User, pk=user_id)

    # Se valida que solo el administrador  pueda editar el perfil de otro usuario.
    # Se valida que solo los administradores puedan editar el perfil de otro usuario.
    if not request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
        if not user == request.user:
            raise Http404

    if request.method == 'POST':
        user_form = EditarAtributosForm(request.POST or None, instance=user, user=request.user)
        #profile_form = ProfileForm(request.POST or None, request.FILES, instance=profile)

        if user_form.is_valid():
            user_form.save()
            #profile_form.save()

            messages.success(request, ('Usuario actualizado'))

            return redirect('users:attribute', user_id)

        else:
            messages.error(request, ('Revisa el formulario e intentalo de nuevo.'))
    else:

        user_form = EditarAtributosForm(
            instance=user,
            user=request.user
        )
        #profile_form = ProfileForm(instance=profile)

    # Obtengo todos los documentos del contrato
    contratos = Contrato.objects.filter(user=user)

    return render(
        request=request,
        template_name='users/users_attribute.html',
        context={
            'usuario': user,
            'form': user_form,
            'contratos': contratos
        }
    )


class PasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/users_password.html'
    success_url = reverse_lazy('home')
    success_message = 'Clave Cambiada Exitosamente'

    def get_success_url(self):
        usuario = self.request.user.id
        return reverse_lazy('users:detail', kwargs={'pk': usuario})


def admin_change_password(request, user_id, template_name='users/users_password.html'):
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            #update_session_auth_hash(request, user)  # Important!

            messages.success(request, 'La clave se actualizo correctamente!')
            return redirect('users:detail', user_id)

    else:
        form = SetPasswordForm(user)

    context = {'form': form, 'user': user, }

    return render(request, template_name, context)


def generar_contrato_usuario(request, user_id, template_name='users/users_generar_contrato.html'):    
    data = dict()
    # Obtengo el usuario
    usuario = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        plantillas_attr = list()
        nuevos = False
        completos = True
        # Obtengo todas las negocios a las que pertenece el usuario.
        negocios = usuario.negocio.all()
        usuario_attr = usuario.atributos
        # Obtengo el set de contrato de la primera negocio relacionada.
        plantillas = Plantilla.objects.filter(activo=True, negocios=negocios[0].id)
        # Obtengo los atributos de cada plantilla
        for p in plantillas:
            plantillas_attr.extend(list(p.atributos))

        if usuario_attr:
            # Creo una lista de los atributos del usuario.
            usr_attr = list(usuario_attr.keys())
            # Obtengo los atributos que no tiene el usuario
            faltantes = [attr for attr in plantillas_attr if attr not in usr_attr]
            # Agrego los atributos al usuario
            if faltantes:
                nuevos = True
                for attr in faltantes:
                    usuario_attr.update({attr: ''})

                data['mensaje'] = 'Trabajador tienen datos incompletos. No se puede generar contrato.'
                data['form_is_valid'] = False

        else:
            nuevos = True
            # Convierto la lista en diccionario
            usuario_attr = dict.fromkeys(plantillas_attr, "")

        if nuevos:
            # Guardo los atributos vacíos en json en el usuario.
            usuario.atributos = usuario_attr
            usuario.save()
            data['mensaje'] = 'Trabajador no tiene la información necesaria para generar set de contrato.'
            data['form_is_valid'] = False
        else:
            # Reviso que todos los atributos tengan datos
            for attr in usuario_attr.items():
                print(attr[0]+' '+attr[1])
                if attr[1] == '':
                    print(attr[0] + ' falta completar')
                    completos = False

                    data['mensaje'] = 'Trabajador no tiene la información necesaria para generar set de contrato.'
                    data['form_is_valid'] = False
                    break

           # Si datos estan completos genero set de contratos del trabajador
            if completos:
                mode = 0o777
                path = os.path.join(settings.MEDIA_ROOT + '/contratos/' + str(user_id))
                # Creo un set de contratos para el usuario
                contrato, created = Contrato.objects.get_or_create(usuario=usuario, estado=Contrato.POR_FIRMAR)
                print('generar contrato con atributos de usuario.')
                if not created:
                    contrato.delete()
                    contrato = Contrato(usuario=usuario)
                    contrato.save()
                # Genero cada documento del set de contratos
                for p in plantillas:
                    documento = MailMerge(p.archivo)
                    documento.merge_pages([usuario_attr])
                    # Si carpeta no existe, crea carpeta de usuario.
                    if not os.path.isdir(path):
                        os.mkdir(path, mode)
                    path_doc = path + '/' + p.tipo.nombre + '.docx'
                    # Creo documento word con datos de usuario
                    documento.write(path_doc)
                    # Convierto documento a PDF
                    pdf = Popen(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', path, path_doc], shell = True)
                    pdf.communicate()

                    path_pdf = 'contratos/' + str(user_id) + '/' + p.tipo.nombre + '.pdf'
                    doc_contrato = DocumentosContrato(contrato=contrato, archivo=path_pdf)
                    doc_contrato.save()

                    # Elimino el documento word.
                    os.remove(path_doc)

                data['form_is_valid'] = True
                data['mensaje'] = 'Para ver el set de contratos presione '
                data['id_contrato'] = contrato.id

    else:
        data['form_is_valid'] = False

    context = {'usuario': usuario, }
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request
    )
    return JsonResponse(data)
