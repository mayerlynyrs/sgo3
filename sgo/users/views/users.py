"""Users views."""


import json
# Djangoogit
import os
import pythoncom
import win32com.client
from docx2pdf import convert
import base64
import requests
from subprocess import Popen
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, F
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from mailmerge import MailMerge
from docxtpl import DocxTemplate
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
# Models
from users.models import User, Trabajador, Sexo, Profesion, ProfesionTrabajador, Especialidad, Contacto, ArchivoTrabajador, ListaNegra
from clientes.models import Cliente, Negocio, Planta
from utils.models import Region, Provincia, Ciudad
from contratos.models import Plantilla, Contrato, DocumentosContrato, ContratosParametrosGen
from examenes.models import Evaluacion
from firmas.models import Firma
# Forms
from users.forms import EditarUsuarioForm, CrearUsuarioForm, CrearTrabajadorForm, EditarTrabajadorForm, ProfesionForm, EspecialidadForm, ProfesionTrabajadorForm, ParentescoCreateForm, ContactoForm, ArchivoTrabajadorForm, ListaNegraForm, EvaluacionAchivoForm
from requerimientos.fecha_a_palabras import fecha_a_letras

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
            # exit()
            user.first_name = request.POST['first_name'].lower()
            user.last_name = request.POST['last_name'].lower()
            email = user.email.lower()
            now_date = datetime.now()
            user.username = email[:email.find('@')] + now_date.strftime("-%y%m%H%M%S")
            user.set_password(user.first_name[0:2].lower()+user.last_name[0:2].lower()+user.rut[0:4])
            user.is_active = True
            user.save()
            user = user_form.save()
            print('userrr', user.id)

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
            messages.error(request, 'Por favor =( revise el formulario e intentelo de nuevo.')
    else:
        user_form = CrearUsuarioForm(user=request.user)
        #profile_form = ProfileForm(initial={'institution': institution}, user=request.user)
    
    return render(request, 'users/users_create.html', {
        'form': user_form,
    })


@login_required
@permission_required('users.add_user', raise_exception=True)
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
        print('paso post')
        user_form = EditarUsuarioForm(request.POST or None, instance=user, user=request.user)
        #profile_form = ProfileForm(request.POST or None, request.FILES, instance=profile)
        print('tambien user_form')

        if user_form.is_valid():
            user.first_name = request.POST['first_name'].lower()
            user.last_name = request.POST['last_name'].lower()
            user.email = user.email.lower()
            user.is_active = True
            user_form.save()
            #profile_form.save()

            # Solo el Administrador puede cambiar el perfil del usuario
            if request.user.groups.filter(name__in=['Administrador', ]).exists():
                user.groups.clear()
                user.groups.add(user_form.cleaned_data['group'])

            messages.success(request, ('Usuario actualizado'))

            if request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
                response = redirect('users:create', user_id)
                return response
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
        template_name='users/create_users.html',
        context={
            'usuario': user,
            'form': user_form,
        }
    )


@login_required(login_url='users:signin')
def update_profile(request, user_id,):
    """Update a user's profile view."""

    user = get_object_or_404(User, pk=user_id)

    # Se valida que solo el administrador  pueda editar el perfil de otro usuario.
    if not request.user.groups.filter(name__in=['Administrador', ]).exists():
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

            if request.user.groups.filter(name__in=['Administrador', ]).exists():
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


class UsersIdView(TemplateView):
    template_name = 'users/create_users.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    try:
        user = get_object_or_404(User, pk=1)
        print("Hay registros!")
    except:
        print("No existen registros")

    def post(self, request, user_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                print(user_id)
                data = []
                for i in Trabajador.objects.filter(user_id=user_id, is_active=True):
                    data.append(i.toJSON())
            elif action == 'contacto_add':
                contact = Contacto()
                contact.nombre = request.POST['nombre'].lower()
                contact.telefono = request.POST['telefono']
                contact.parentesco_id = request.POST['parentesco']
                contact.user_id = user_id
                if Contacto.objects.filter(telefono=request.POST['telefono'], user_id=user_id).exists():
                    print('si existe')
                    messages.success(request, 'El fono ya esta ingresado para este trabajador.')
                else:
                    print('no existe')
                    contact.save()
                    print('save')
            elif action == 'contacto_edit':
                contact = Contacto.objects.get(pk=request.POST['id'])
                contact.nombre = request.POST['nombre'].lower()
                contact.telefono = request.POST['telefono']
                contact.parentesco_id = request.POST['parentesco']
                contact.user_id = user_id
                contact.save()
            elif action == 'contacto_delete':
                contact = Contacto.objects.get(pk=request.POST['id'])
                contact.status = False
                contact.save()
            elif action == 'profesion_add':
                profes = ProfesionTrabajador()
                profes.egreso = request.POST['egreso']
                profes.institucion = request.POST['institucion'].lower()
                profes.profesion_id = request.POST['profesion']
                profes.user_id = user_id
                profes.save()
            elif action == 'profesion_edit':
                profes = ProfesionTrabajador.objects.get(pk=request.POST['id'])
                profes.egreso = request.POST['egreso']
                profes.institucion = request.POST['institucion'].lower()
                profes.profesion_id = request.POST['profesion']
                profes.user_id = user_id
                profes.save()
            elif action == 'profesion_delete':
                profes = ProfesionTrabajador.objects.get(pk=request.POST['id'])
                profes.status = False
                profes.save()
            elif action == 'archivo_add':
                archiv = ArchivoTrabajador()
                archiv.tipo_archivo_id = request.POST['tipo_archivo']
                archiv.archivo = request.FILES['archivo']
                archiv.user_id = user_id
                archiv.save()
            elif action == 'archivo_delete':
                archiv = ArchivoTrabajador.objects.get(pk=request.POST['id'])
                archiv.status = False
                archiv.save()
            elif action == 'evaluacion_add':
                evalu = Evaluacion()
                evalu.fecha_examen = request.POST['fecha_examen']
                evalu.fecha_vigencia = request.POST['fecha_vigencia']
                evalu.descripcion = request.POST['descripcion']
                if "referido" in request.POST:
                    estado = True
                    evalu.referido =  estado
                else:
                    estado = False
                    evalu.referido =  estado
                evalu.valor_examen = request.POST['valor_examen']
                evalu.resultado = request.POST['resultado']
                evalu.planta_id = request.POST['planta']
                evalu.examen_id = request.POST['examen']
                evalu.archivo = request.FILES['archivo']
                evalu.user_id = user_id
                evalu.save()
            elif action == 'evaluacion_edit':
                evalu = Evaluacion.objects.get(pk=request.POST['id'])
                evalu.fecha_examen = request.POST['fecha_examen']
                evalu.fecha_vigencia = request.POST['fecha_vigencia']
                evalu.descripcion = request.POST['descripcion']
                if "referido" in request.POST:
                    estado = True
                    evalu.referido =  estado
                else:
                    estado = False
                    evalu.referido =  estado
                evalu.valor_examen = request.POST['valor_examen']
                evalu.resultado = request.POST['resultado']
                evalu.planta_id = request.POST['planta']
                evalu.examen_id = request.POST['examen']
                evalu.archivo = request.FILES['archivo']
                evalu.user_id = user_id
                evalu.save()
            elif action == 'evaluacion_delete':
                evalu = Evaluacion.objects.get(pk=request.POST['id'])
                evalu.status = False
                evalu.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        # return JsonResponse({'data': 'data'},{'data2': 'data2'})
        # return JsonResponse(data, safe=False)

    def get_context_data(request, user_id, **kwargs):

        try:
            user = get_object_or_404(User, pk=user_id)
            print("Hay registros!")
        except:
            print("No existen registros")

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

            user_form = EditarUsuarioForm(instance=user, user=request.user)
            #profile_form = ProfileForm(request.POST or None, request.FILES, instance=profile)

            if user_form.is_valid():
                user.first_name = request.POST['first_name'].lower()
                user.last_name = request.POST['last_name'].lower()
                user.email = request.POST['email'].lower()
                user.is_active = True
                user_form.save()
                #profile_form.save()

                # Solo el Administrador puede cambiar el perfil del usuario
                if request.user.groups.filter(name__in=['Administrador', ]).exists():
                    user.groups.clear()
                    user.groups.add(user_form.cleaned_data['group'])

                messages.success(request, ('Usuario actualizado'))

                if request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
                    response = redirect('users:update', user_id)
                    return response
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
        
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Contactos'
        context['list_url'] = reverse_lazy('users:<int:user_id>/create')
        context['update_url'] = reverse_lazy('users:update')
        context['entity'] = 'Contactos'
        context['usuario'] = user
        context['user_id'] = user_id
        context['form'] = user_form
        context['form2'] = ContactoForm()
        context['form3'] = ProfesionTrabajadorForm()
        context['form4'] = ArchivoTrabajadorForm()
        context['form5'] = EvaluacionAchivoForm()
        return context


class TrabajadorDetailView(LoginRequiredMixin, DetailView):
    model = Trabajador
    template_name = "users/users_detail.html"
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super(TrabajadorDetailView, self).get_context_data(**kwargs)

        # Se valida que solo el administrador pueda editar el perfil de otro usuario.
        if not self.request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT',]).exists():
            if not self.object == self.request.user:
                raise Http404

        return context


class TrabajadoresIdView(TemplateView):
    template_name = 'users/create_trabajadores.html'
    # template_name = 'users/create_users.html'
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    try:
        user = get_object_or_404(User, pk=1)
        print("Hay registros!")
    except:
        print("No existen registros")

    def post(self, request, user_id, *args, **kwargs):

        # Se obtiene el perfil y las plantas del usuario.
        try:
            plantas_usuario = Planta.objects.values_list('id', flat=True).filter(user=user_id)
            #plantas_usuario[::1]
        except:
            plantas_usuario = ''
        
        trabajador2 = Trabajador.objects.get(user_id=user_id, is_active=True)
        print('trabajador2', trabajador2)
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Trabajador.objects.filter(user_id=user_id, is_active=True):
                    data.append(i.toJSON())
            elif action == 'contacto_add':
                contact = Contacto()
                contact.nombre = request.POST['nombre'].lower()
                contact.telefono = request.POST['telefono']
                contact.parentesco_id = request.POST['parentesco']
                print("contacto trab",trabajador2.id)
                contact.trabajador_id = trabajador2.id

                if Contacto.objects.filter(telefono=request.POST['telefono'], trabajador_id=trabajador2.id).exists():
                    print('si existe')
                    messages.success(request, 'El fono ya esta ingresado para este trabajador.')
                else:
                    print('no existe')
                    contact.save()
                    print('save')
            elif action == 'contacto_edit':
                contact = Contacto.objects.get(pk=request.POST['id'])
                contact.nombre = request.POST['nombre'].lower()
                contact.telefono = request.POST['telefono']
                contact.parentesco_id = request.POST['parentesco']
                contact.trabajador_id = trabajador2.id
                contact.save()
            elif action == 'contacto_delete':
                contact = Contacto.objects.get(pk=request.POST['id'])
                contact.status = False
                contact.save()
            elif action == 'profesion_add':
                profes = ProfesionTrabajador()
                profes.egreso = request.POST['egreso']
                profes.institucion = request.POST['institucion'].lower()
                profes.profesion_id = request.POST['profesion']
                profes.trabajador_id = trabajador2.id
                profes.save()
            elif action == 'profesion_edit':
                profes = ProfesionTrabajador.objects.get(pk=request.POST['id'])
                profes.egreso = request.POST['egreso']
                profes.institucion = request.POST['institucion'].lower()
                profes.profesion_id = request.POST['profesion']
                profes.trabajador_id = trabajador2.id
                profes.save()
            elif action == 'profesion_delete':
                profes = ProfesionTrabajador.objects.get(pk=request.POST['id'])
                profes.status = False
                profes.save()
            elif action == 'archivo_add':
                archiv = ArchivoTrabajador()
                archiv.tipo_archivo_id = request.POST['tipo_archivo']
                archiv.archivo = request.FILES['archivo']
                archiv.trabajador_id = trabajador2.id
                archiv.save()
            elif action == 'archivo_delete':
                archiv = ArchivoTrabajador.objects.get(pk=request.POST['id'])
                archiv.status = False
                archiv.save()
            elif action == 'evaluacion_add':
                evalu = Evaluacion()
                evalu.fecha_examen = request.POST['fecha_examen']
                evalu.fecha_vigencia = request.POST['fecha_vigencia']
                evalu.descripcion = request.POST['descripcion']
                if "referido" in request.POST:
                    estado = True
                    evalu.referido =  estado
                else:
                    estado = False
                    evalu.referido =  estado
                evalu.valor_examen = request.POST['valor_examen']
                evalu.resultado = request.POST['resultado']
                evalu.planta_id = request.POST['planta']
                evalu.examen_id = request.POST['examen']
                evalu.archivo = request.FILES['archivo']
                evalu.trabajador_id = trabajador2.id
                evalu.save()
            elif action == 'evaluacion_edit':
                evalu = Evaluacion.objects.get(pk=request.POST['id'])
                evalu.fecha_examen = request.POST['fecha_examen']
                evalu.fecha_vigencia = request.POST['fecha_vigencia']
                evalu.descripcion = request.POST['descripcion']
                if "referido" in request.POST:
                    estado = True
                    evalu.referido =  estado
                else:
                    estado = False
                    evalu.referido =  estado
                evalu.valor_examen = request.POST['valor_examen']
                evalu.resultado = request.POST['resultado']
                evalu.planta_id = request.POST['planta']
                evalu.examen_id = request.POST['examen']
                evalu.archivo = request.FILES['archivo']
                evalu.trabajador_id = trabajador2.id
                evalu.save()
            elif action == 'evaluacion_delete':
                evalu = Evaluacion.objects.get(pk=request.POST['id'])
                evalu.status = False
                evalu.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        # return JsonResponse({'data': 'data'},{'data2': 'data2'})
        # return JsonResponse(data, safe=False)

    def get_context_data(request, user_id, **kwargs):

        trabajador = get_object_or_404(Trabajador, user_id=user_id)
        usuario_trabajador = get_object_or_404(Trabajador, user=user_id)
        user = get_object_or_404(User, pk=user_id)

        # Se obtiene las plantas del usuario trabajador.
        try:
            plantas_usuario = Planta.objects.values_list('id', flat=True).filter(user=user_id)
            #plantas_usuario[::1]
        except:
            plantas_usuario = ''

        # trabajador2 = Trabajador.objects.get(user_id=user_id, is_active=True)
      
        
        trabajador_form = EditarTrabajadorForm(
            instance=trabajador,
            initial={'planta': list(plantas_usuario), },
            trabajador=request.user,
            user=request.user,
            usuario_trabajador=usuario_trabajador.user.id
            )
      

        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Trabajadores'
        context['list_url'] = reverse_lazy('users:<int:user_id>/create')
        context['update_url'] = reverse_lazy('users:create_trabajador')
        context['entity'] = 'Trabajador'
        context['usuario'] = user
        context['trabajador'] = trabajador
        context['trabajador_id'] = trabajador.id
        context['form'] = trabajador_form
        context['form2'] = ContactoForm()
        context['form3'] = ProfesionTrabajadorForm()
        context['form4'] = ArchivoTrabajadorForm()
        context['form5'] = EvaluacionAchivoForm()
        return context


class TrabajadorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Trabajador
    template_name = "users/trabajadores_list.html"
    paginate_by = 25
    ordering = ['first_name', 'last_name']

    permission_required = 'users.view_trabajador'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(TrabajadorListView, self).get_context_data(**kwargs)

        if self.request.user.groups.filter(name__in=['Trabajador']).exists():
            institutions = Planta.objects.values(
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
            # No es Trabajador y recibe parametro de busqueda
            if not self.request.user.groups.filter(name__in=['Trabajador', ]).exists():
                queryset = Trabajador.objects.select_related('user').filter(
                    Q(cliente__in=self.request.user.cliente.all()),
                    Q(planta__in=self.request.user.planta.all()),
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search) |
                    Q(terminos_condiciones__icontains=search) |
                    Q(username__icontains=search)).exclude(
                    groups__name__in=['Administrador', 'Administrador Contratos', 'Jefe RRHH', 'Analista Operación', 'Analista RRHH', 'Psicologo']).order_by(
                    'first_name', 'last_name').distinct('first_name', 'last_name')
            else:
                # Es Trabajador y recibe parametro de busqueda
                queryset = super(TrabajadorListView, self).get_queryset().filter(
                                        Q(first_name__icontains=search) |
                                        Q(last_name__icontains=search) |
                                        Q(rut__icontains=search) |
                                        Q(groups__name__icontains=search) |
                                        Q(username__icontains=search)).order_by(
                    'first_name', 'last_name').distinct('first_name', 'last_name')
        else:
            # Perfil no es Trabajador
            if not self.request.user.groups.filter(name__in=['Trabajador']).exists():
                if planta is None:
                    queryset = Trabajador.objects.filter(
                        user__planta__in=self.request.user.planta.all()).exclude(
                        user__groups__name__in=['Administrador', 'Administrador Contratos', 'Jefe RRHH', 'Analista Operación', 'Analista RRHH',
                        'Psicologo', 'Fiscalizador DT', 'Fiscalizador Interno']).order_by(
                        'user__first_name', 'user__last_name').distinct('user__first_name', 'user__last_name')
                else:
                    # No es Trabajador y hay plantas seleccionadas
                    queryset = Trabajador.objects.filter(
                        user__planta__in=planta).exclude(
                        user__groups__name__in=['Administrador', 'Administrador Contratos', 'Jefe RRHH', 'Analista Operación', 'Analista RRHH', 'Psicologo']).order_by(
                        'user__first_name', 'user__last_name').distinct('user__first_name', 'user__last_name')

            else:
                # Es administrador y no hay planta seleccionada.
                if planta is None:
                    queryset = super(TrabajadorListView, self).get_queryset().order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')
                else:
                    # Es administrador y hay plantas seleccionadas.
                    queryset = super(TrabajadorListView, self).get_queryset().filter(
                        planta__in=planta).order_by(
                        'first_name', 'last_name').distinct('first_name', 'last_name')

        return queryset


@login_required
@permission_required('users.add_trabajador', raise_exception=True)
def create_trabajador(request):
    if request.method == 'POST':
        trabajador_form = CrearTrabajadorForm(data=request.POST, user=request.user)

        if trabajador_form.is_valid():       
            user = User()
            user.rut = request.POST['rut']
            user.first_name = request.POST['first_name'].lower()
            user.last_name = request.POST['last_name'].lower()
            user.fecha_nacimiento = request.POST['fecha_nacimiento']
            user.telefono = request.POST['telefono']
            user.email = request.POST['email'].lower()
            email = user.email
            now_date = datetime.now()
            user.username = email[:email.find('@')] + now_date.strftime("-%y%m%H%M%S")
            user.set_password(user.first_name[0:2].lower()+user.last_name[0:2].lower()+user.rut[0:4])
            # user.cliente = request.POST['cliente']
            # user.planta = request.POST['planta']
            user.is_superuser = False
            user.is_staff = False
            user.is_active = True
            user.save()
            # Perfil
            group = request.POST.getlist('group')
            for i in group:
                user.groups.add(i)
            # Planta
            plant = request.POST.getlist('planta')
            for i in plant:
                user.planta.add(i)

                    
            trabajador = trabajador_form.save(commit=False)
            trabajador.first_name = request.POST['first_name'].lower()
            trabajador.last_name = request.POST['last_name'].lower()
            trabajador.email = request.POST['email'].lower()
            trabajador.is_active = True
            trabajador.user_id = user.id
            trabajador.save()
            trabajador = trabajador_form.save()

            # Enviar correo con Términos y Condiciones al Trabajador (terminos_condiciones)
            fecha_registro_palabras = fecha_a_letras(trabajador.created)
            # subject, from_email, to = 'Creación de Trabajador en SGO3 | Términos y Condiciones', 'soporte@empresasintegra.cl', trabajador.email
            # text_content = 'No responder este Mensaje.'
            # html_content = 'Estimado(a) por medio del presente se le informa que al día ' + str(fecha_registro_palabras) + ' se ha creado como Trabajador del Sistema de Gestión de Operaciones (SGO3), por favor lea el documento adjunto y acepte los TÉRMINOS LEGALES Y CONDICIONES GENERALES DE USO DEL SITIO WEB </br></br><p><a href="http://192.168.0.201:8000/users/' + str(trabajador.id) + '/terminos_condiciones/" style="padding: 11px 20px; margin: 16px 0px 25px; font-size: 14px; color: #fff; background: #008a8a; border-radius: 5px; text-decoration:none; font-weight: bold;"> Aceptar Términos y Condiciones</a></p>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            send_mail(
                'Creación de Trabajador en SGO3',
                'Estimado(a) ' + str(trabajador.first_name.title() + ' ' + trabajador.last_name.title()) + ' por '
                'medio del presente se le informa que al día ' + str(fecha_registro_palabras) + ' usted se ha '
                'creado como Trabajador en el Sistema de Gestión de Operaciones (SGO3)',
                trabajador.created_by.email,
                [trabajador.email, 'soporte@empresasintegra.cl'], fail_silently=False,
            )

            messages.success(request, 'Trabajador Creado Exitosamente')
            return redirect('users:create_trabajador', user.id)
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
 
    else:
        trabajador_form = CrearTrabajadorForm(user=request.user)
    
    return render(request, 'users/trabajadores_create.html', {
        'form': trabajador_form,
    })


@login_required
@permission_required('users.add_user', raise_exception=True)
def update_trabajador(request, trabajador_id):
    """Update a user's profile view."""

    user = get_object_or_404(Trabajador, pk=trabajador_id)

    usuario = get_object_or_404(User, pk=user.user_id)
    pk = Trabajador.objects.values_list('user_id', flat=True).get(pk=trabajador_id)

    # Se valida que solo el administrador  pueda editar el perfil de otro usuario.
    # Se valida que solo los administradores puedan editar el perfil de otro usuario.
    if not request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
        if not user == request.user:
            raise Http404

    if request.method == 'POST':
        trabajador_form = EditarTrabajadorForm(request.POST or None, instance=user, user=request.user)

        if trabajador_form.is_valid():
            user.first_name = request.POST['first_name'].lower()
            user.last_name = request.POST['last_name'].lower()
            user.email = request.POST['email'].lower()
            user.is_active = True
            trabajador_form.save()
            usuario.first_name = request.POST['first_name'].lower()
            usuario.last_name = request.POST['last_name'].lower()
            usuario.email = request.POST['email'].lower()
            usuario.telefono = request.POST['telefono']
            plantas = []
            for d in usuario.planta.all():
                plantas.append(d.id ) 
            for a in plantas:
                usuario.planta.remove(a)
            plant = request.POST.getlist('planta')
            for i in plant:
                usuario.planta.add(i)


            usuario.save()
            messages.success(request, ('Trabajador actualizado'))

            if request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', ]).exists():
                response = redirect('users:create_trabajador', pk)
                return response
            else:
                return redirect('home')

        else:
            messages.error(request, ('Revisa el formulario e intentalo de nuevo.'))
    else:

        trabajador_form = EditarTrabajadorForm(
            instance=user,
            user=request.user
        )

    return render(
        request=request,
        template_name='users/create_trabajadores.html',
        context={
            'trabajador': user,
            'form': trabajador_form,
        }
    )


@login_required
@permission_required('users.add_user', raise_exception=True)
def autorizacion_trabajador(request, trabajador_id):
    """Autorización a Employee view."""

    # Busca si existe la plantilla de Autorización Firma Electrónica (12)
    if not Plantilla.objects.filter(tipo_id=12).exists():
        messages.error(request, 'No existe la plantilla asociada. Por favor gestionar con el Dpto. de Contratos')
        return redirect('users:list_trabajador')
    else:
        employee = Trabajador.objects.get(user=trabajador_id, is_active=True)
        employee.terminos_condiciones = True
        employee.save()
        # Trae la plantilla de Autorización Firma Electrónica (12)
        formato = Plantilla.objects.values('archivo', 'abreviatura', 'tipo_id').filter(tipo_id=12)
        now = datetime.now()
        for formt in formato:
            doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT + '/' + formt['archivo']))
            # Variables de Autorización Firma Electrónica
            context = { 'fecha_creacion': employee.created.strftime("%A,%d %B, %Y"),
                        'rut_trabajador': employee.rut,
                        'nombres_trabajador': employee.first_name.title(),
                        'apellidos_trabajador': employee.last_name.title(),
                        'correo_trabajador': employee.email,
                        'telefono_trabajador': employee.telefono,
                        }
            rut_trabajador = employee.rut
            doc.render(context)
            # Contratos Parametros General, ruta_documentos donde guardara el documento
            ruta_documentos = ContratosParametrosGen.objects.values_list('ruta_documentos', flat=True).get(pk=1, status=True)
            path = os.path.join(ruta_documentos)
            # Si carpeta no existe, crea carpeta de contratos.
            carpeta = 'autorizaciones'

            try:
                os.mkdir(path + carpeta)
                path = os.path.join(settings.MEDIA_ROOT + '/autorizaciones/')
                doc.save(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(trabajador_id)  + '.docx')
                win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
                # convert("Contrato#1.docx")

                convert(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(trabajador_id) + ".docx", path +  str(rut_trabajador) + "_" + formt['abreviatura'] + "_" +  str(trabajador_id) + ".pdf")                
                # Elimino el documento word.
                os.remove(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(trabajador_id) + '.docx')
                # Inicio integración de la API
                nombre_archivo = str(rut_trabajador) + "_" + formt['abreviatura'] + "_" +  str(trabajador_id) + ".pdf"
                ubicacion = path + nombre_archivo
                with open(ubicacion, "rb") as pdf_file:
                    documento = base64.b64encode(pdf_file.read()).decode('utf-8')
                document = f'{documento}'
                
                url = "https://app.ecertia.com/api/EviSign/Submit"

                payload = json.dumps({
                "Subject": "Autorización Firma Electrónica Trabajador del SGO3",
                "Document": document,
                "SigningParties": {
                    "Name": employee.first_name.title() + ' ' + employee.last_name.title(),
                    "Address": employee.email,
                    "SigningMethod": "Email Pin"
                },
                "Options": {
                    "TimeToLive": 1200,
                    "RequireCaptcha": False,
                    "NotaryRetentionPeriod": 0,
                    "OnlineRetentionPeriod": 1
                },
                "Issuer": "EVISA"
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': 'Basic bWF5ZXJseW4ucm9kcmlndWV6QGVtcHJlc2FzaW50ZWdyYS5jbDppbnRlZ3JhNzYyNQ==',
                    'Cookie': 'X-UAId=1237; ss-id=kEDBUDCvtQL/m68MmIoY; ss-pid=fogDX+U1tusPTqHrA4eF'
                            }

                response = requests.request("POST", url, headers=headers, data=payload)

                print('API', response.text)
                api = Firma()
                api.respuesta_api = response.text
                api.rut_trabajador = rut_trabajador
                api.estado_firma_id = 1
                api.fecha_envio = now
                api.status = True
                api.save()
                messages.success(request, 'Autorización de Firma Electrónica enviada Exitosamente')
            except:
                path = os.path.join(settings.MEDIA_ROOT + '/autorizaciones/')
                doc.save(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(trabajador_id)  + '.docx')
                win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())

                convert(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(trabajador_id) + ".docx", path +  str(rut_trabajador) + "_" + formt['abreviatura'] + "_" +  str(trabajador_id) + ".pdf")                
                # Elimino el documento word.
                os.remove(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(trabajador_id) + '.docx')
                # Inicio integración de la API
                nombre_archivo = str(rut_trabajador) + "_" + formt['abreviatura'] + "_" +  str(trabajador_id) + ".pdf"
                ubicacion = path + nombre_archivo
                with open(ubicacion, "rb") as pdf_file:
                    documento = base64.b64encode(pdf_file.read()).decode('utf-8')
                document = f'{documento}'
                
                url = "https://app.ecertia.com/api/EviSign/Submit"

                payload = json.dumps({
                "Subject": "Autorización Firma Electrónica Trabajador del SGO3",
                "Document": document,
                "SigningParties": {
                    "Name": employee.first_name.title() + ' ' + employee.last_name.title(),
                    "Address": employee.email,
                    "SigningMethod": "Email Pin"
                },
                "Options": {
                    "TimeToLive": 1200,
                    "RequireCaptcha": False,
                    "NotaryRetentionPeriod": 0,
                    "OnlineRetentionPeriod": 1
                },
                "Issuer": "EVISA"
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': 'Basic bWF5ZXJseW4ucm9kcmlndWV6QGVtcHJlc2FzaW50ZWdyYS5jbDppbnRlZ3JhNzYyNQ==',
                    'Cookie': 'X-UAId=1237; ss-id=kEDBUDCvtQL/m68MmIoY; ss-pid=fogDX+U1tusPTqHrA4eF'
                            }

                response = requests.request("POST", url, headers=headers, data=payload)

                print('API', response.text)
                api = Firma()
                api.respuesta_api = response.text
                api.rut_trabajador = rut_trabajador
                api.estado_firma_id = 1
                api.fecha_envio = now
                api.status = True
                api.save()
                messages.success(request, 'Autorización de Firma Electrónica enviada Exitosamente')
        
        return redirect('users:list_trabajador')


class ContactoView(TemplateView):
    """Profesion List
    Vista para listar todos los profesion según el usuario y sus las negocios
    relacionadas.
    """
    template_name = 'users/create_users.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, user_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata2':
                data = []
                for i in Contacto.objects.filter(trabajador_id=user_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class ProfesionTrabajadorView(TemplateView):
    """Profesion List
    Vista para listar todos los profesion según el usuario y sus las negocios
    relacionadas.
    """
    template_name = 'users/create_users.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, user_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata3':
                data = []
                for i in ProfesionTrabajador.objects.filter(trabajador_id=user_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)



class ArchivoTrabajadorView(TemplateView):
    """Profesion List
    Vista para listar todos los profesion según el usuario y sus las negocios
    relacionadas.
    """
    template_name = 'users/create_users.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, user_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata4':
                data = []
                for i in ArchivoTrabajador.objects.filter(trabajador=user_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            print(e)
        return JsonResponse(data, safe=False)



class EvaluacionUserView(TemplateView):
    """Profesion List
    Vista para listar todos los profesion según el usuario y sus las negocios
    relacionadas.
    """
    template_name = 'users/create_users.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, user_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata5':
                data = []
                for i in Evaluacion.objects.filter(trabajador=user_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            print(e)
        return JsonResponse(data, safe=False)


class ProfesionView(TemplateView):
    """Profesion List
    Vista para listar todos los profesion según el usuario y sus las negocios
    relacionadas.
    """
    template_name = 'users/profesion_list.html'

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
                for i in Profesion.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                espec = Profesion()
                espec.nombre = request.POST['nombre'].lower()
                espec.status = True
                # espec.created_date = request.POST['created_date']
                espec.save()
            elif action == 'edit':
                espec = Profesion.objects.get(pk=request.POST['id'])
                espec.nombre = request.POST['nombre'].lower()
                espec.save()
            elif action == 'delete':
                espec = Profesion.objects.get(pk=request.POST['id'])
                espec.status = False
                espec.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Profesion'
        context['list_url'] = reverse_lazy('users:profesion')
        context['entity'] = 'Profesiones'
        context['form'] = ProfesionForm()
        return context


class EspecialidadView(TemplateView):
    template_name = 'users/especialidad_list.html'

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
                for i in Especialidad.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                espec = Especialidad()
                espec.nombre = request.POST['nombre'].lower()
                espec.status = True
                # espec.created_date = request.POST['created_date']
                espec.save()
            elif action == 'edit':
                espec = Especialidad.objects.get(pk=request.POST['id'])
                espec.nombre = request.POST['nombre'].lower()
                espec.save()
            elif action == 'delete':
                espec = Especialidad.objects.get(pk=request.POST['id'])
                espec.status = False
                espec.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Especialidades'
        context['list_url'] = reverse_lazy('users:especialidad')
        context['entity'] = 'Especialidades'
        context['form'] = EspecialidadForm()
        return context


class ListaNegraView(TemplateView):
    template_name = 'users/lista_negra_list.html'
    

    permission_required = 'users.lista_negra'
    raise_exception = True

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
                for i in ListaNegra.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                lnegra = ListaNegra()
                lnegra.tipo = request.POST['tipo']
                lnegra.descripcion = request.POST['descripcion']
                lnegra.trabajador_id = request.POST['trabajador']
                if request.POST['tipo'] == 'LN':
                    lnegra.planta_id = None
                else:
                    lnegra.planta_id = request.POST['planta']
                lnegra.status = True
                # lnegra.created_date = request.POST['created_date']
                lnegra.save()
            elif action == 'edit':
                lnegra = ListaNegra.objects.get(pk=request.POST['id'])
                lnegra.tipo = request.POST['tipo']
                lnegra.descripcion = request.POST['descripcion']
                lnegra.trabajador_id = request.POST['trabajador']
                lnegra.planta_id = request.POST['planta']
                lnegra.save()
            elif action == 'delete':
                lnegra = ListaNegra.objects.get(pk=request.POST['id'])
                lnegra.status = False
                lnegra.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Lista Negra'
        context['list_url'] = reverse_lazy('users:lista_negra')
        context['entity'] = 'ListaNegra'
        context['form'] = ListaNegraForm()
        return context


class TerminosCondicionView(TemplateView):
    model = Trabajador
    template_name = 'emails/terms_conditions_form.html'
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super(TerminosCondicionView, self).get_context_data(**kwargs)

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
