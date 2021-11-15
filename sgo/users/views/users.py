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
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from mailmerge import MailMerge
from django.conf import settings
# Models
from users.models import Sexo
from utils.models import Cliente, Planta, Region, Provincia, Ciudad
from contratos.models import Plantilla, Contrato, DocumentosContrato
# Forms
from users.forms import EditarAtributosForm, EditarUsuarioForm, CrearUsuarioForm

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

# Planta
def load_plantas(request):
    cliente_id = request.GET.get('cliente')    
    plantas = Planta.objects.filter(cliente_id=cliente_id).order_by('nombre')
    context = {'plantas': plantas}
    return render(request, 'users/planta.html', context)


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
            institutions = Planta.objects.values(
                    value=F('id'),
                    title=F('nombre')).all().order_by('nombre')
                #cache.set('institutions', institutions)
            institutions = Sexo.objects.values(
                    value=F('id'),
                    title=F('nombre')).all().order_by('nombre')

            context['plantas'] = institutions
            context['planta'] = self.kwargs.get('planta_id', None)

        return context

    def get_queryset(self):
        search = self.request.GET.get('q')
        planta = self.kwargs.get('planta_id', None)

        if planta == '':
            planta = None

        if search:
            # No es administrador y recibe parametro de busqueda
            if not self.request.user.groups.filter(name__in=['Administrador', ]).exists():
                queryset = User.objects.select_related('planta').filter(
                    Q(cliente__in=self.request.user.cliente.all()),
                    Q(planta__in=self.request.user.planta.all()),
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
                if planta is None:
                    queryset = User.objects.filter(
                        planta__in=self.request.user.planta.all()).exclude(
                        groups__name__in=['Administrador']).order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')
                else:
                    # No es administrador y hay plantas seleccionadas
                    queryset = User.objects.filter(
                        planta__in=planta).exclude(
                        groups__name__in=['Administrador']).order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')

            else:
                # Es administrador y no hay planta seleccionada.
                if planta is None:
                    queryset = super(UserListView, self).get_queryset().order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')
                else:
                    # Es administrador y hay plantas seleccionadas.
                    queryset = super(UserListView, self).get_queryset().filter(
                        planta__in=planta).order_by(
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
            print(request.POST.getlist('group'))
            if request.POST.getlist('group') == ['1']:
                user.is_superuser = True
                user.is_staff = True
                user.atributos = 'NO APLICA'
            # exit()
            email = user.email
            now_date = datetime.now()
            user.username = email[:email.find('@')] + now_date.strftime("-%y%m%H%M%S")
            user.set_password(user.first_name[0:2].lower()+user.last_name[0:2].lower()+user.rut[0:4])
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
            return redirect('users:list')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        user_form = CrearUsuarioForm(user=request.user)
        #profile_form = ProfileForm(initial={'institution': institution}, user=request.user)
    
    return render(request, 'users/users_create.html', {
        'form': user_form,
    })


@login_required(login_url='users:signin')
def update_user(request, user_id):
    """Update a user's profile view."""

    user = get_object_or_404(User, pk=user_id)

    # Se valida que solo el administrador  pueda editar el perfil de otro usuario.
    # Se valida que solo los administradores puedan editar el perfil de otro usuario.
    if not request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
        if not user == request.user:
            raise Http404

    # Se obtiene el perfil y las plantas del usuario.
    try:
        current_group = user.groups.get()
        plantas_usuario = Planta.objects.values_list('id', flat=True).filter(user=user_id)
        #plantas_usuario[::1]
    except:
        current_group = ''
        plantas_usuario = ''

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
            initial={'group': current_group.pk, 'planta': list(plantas_usuario), },
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
    contratos = Contrato.objects.filter(usuario=user)

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
        # Obtengo todas las plantas a las que pertenece el usuario.
        plantas = usuario.planta.all()
        usuario_attr = usuario.atributos
        # Obtengo el set de contrato de la primera planta relacionada.
        plantillas = Plantilla.objects.filter(activo=True, plantas=plantas[0].id)
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
