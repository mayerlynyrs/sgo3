"""Contratos views."""

import os
# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.views.generic import TemplateView
from django.db.models import Count
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from mailmerge import MailMerge
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
# Models
from ficheros.models import Fichero
from contratos.models import Contrato, DocumentosContrato, ContratosBono
from requerimientos.models import RequerimientoTrabajador
# Form
from contratos.forms import CrearContratoForm
from requerimientos.forms import RequeriTrabajadorForm
from users.forms import EditarUsuarioForm


class ContratoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Contrato List
    Vista para listar todos las contratos según el usuario y plantas.
    """
    model = Contrato
    template_name = "contratos/contrato_list.html"
    paginate_by = 25
    #ordering = ['plantas', 'nombre', ]

    permission_required = 'contratos.view_contrato'
    raise_exception = True

    def get_queryset(self):
        search = self.request.GET.get('q')
        planta = self.kwargs.get('planta_id', None)

        if planta == '':
            planta = None

        if search:
            # Si el usuario no administrador se despliegan todos los contratos
            # de las plantas a las que pertenece el usuario, según el critero de busqueda.
            if not self.request.user.groups.filter(name__in=['Administrador', ]).exists():
                queryset = super(ContratoListView, self).get_queryset().filter(
                    Q(usuario__planta__in=self.request.user.planta.all()),
                    Q(usuario__first_name__icontains=search),
                    Q(usuario__last_name__icontains=search)
                ).distinct()
            else:
                # Si el usuario es administrador se despliegan todos las plantillas
                # segun el critero de busqueda.
                queryset = super(ContratoListView, self).get_queryset().filter(
                    Q(usuario__first_name__icontains=search),
                    Q(usuario__last_name__icontains=search),
                    Q(id__icontains=search),
                    Q(estado__icontains=search)
                ).distinct()
        else:
            # Si el usuario no es administrador, se despliegan los contrtatos
            # de las plantas a las que pertenece el usuario.
            if not self.request.user.groups.filter(name__in=['Administrador']).exists():
                queryset = super(ContratoListView, self).get_queryset().filter(
                    Q(user__planta__in=self.request.user.planta.all()),
                ).distinct()
            else:
                # Si el usuario es administrador, se despliegan todos los contratos.
                if planta is None:
                    queryset = super(ContratoListView, self).get_queryset()
                else:
                    # Si recibe la planta, solo muestra las plantillas que pertenecen a esa planta.
                    queryset = super(ContratoListView, self).get_queryset().filter(
                        Q(user__planta__in=self.request.user.planta.all())
                    ).distinct()

        return queryset


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def create(request):
    if request.method == 'POST':

        form = CrearContratoForm(data=request.POST, files=request.FILES, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Contrato Creado Exitosamente')

            return redirect('contratos:list-plantilla')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = CrearContratoForm(user=request.user)

    return render(request, 'contratos/contrato_create.html', {
        'form': form,
    })


class ContratoIdView(TemplateView):
    template_name = 'contratos/create_contrato.html'
    # requerimiento_trabajador_id=Contrato
    
    # # cliente = get_object_or_404(Contrato, pk=1)

    # @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    # def post(self, request, requerimiento_trabajador_id, *args, **kwargs):
    #     data = {}
    #     try:
    #         action = request.POST['action']
    #         if action == 'searchdata':
    #             print(requerimiento_trabajador_id)
    #             data = []
    #             for i in RequerimientoTrabajador.objects.filter(id=requerimiento_trabajador_id, status=True):
    #                 data.append(i.toJSON())
    #         elif action == 'negocio_add':
    #             negocio = ContratosBono()
    #             negocio.nombre = request.POST['nombre']
    #             negocio.descripcion = request.POST['descripcion']
    #             negocio.archivo = request.FILES['archivo']
    #             negocio.requerimiento_trabajador_id = requerimiento_trabajador_id
    #             negocio.save()
    #         elif action == 'negocio_edit':
    #             negocio = ContratosBono.objects.get(pk=request.POST['id'])
    #             negocio.nombre = request.POST['nombre']
    #             negocio.descripcion = request.POST['descripcion']
    #             negocio.archivo = request.FILES['archivo']
    #             negocio.requerimiento_trabajador_id = requerimiento_trabajador_id
    #             negocio.save()
    #         elif action == 'negocio_delete':
    #             negocio = ContratosBono.objects.get(pk=request.POST['id'])
    #             negocio.status = False
    #             negocio.save()
    #         else:
    #             data['error'] = 'Ha ocurrido un error'
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data, safe=False)


    def get_context_data(self, requerimiento_trabajador_id, **kwargs):

        requer_user = get_object_or_404(RequerimientoTrabajador, pk=requerimiento_trabajador_id)
        trabaj = RequerimientoTrabajador.objects.filter(id=requerimiento_trabajador_id).values(
                'user__first_name', 'user__last_name', 'user__rut','user__estado_civil__nombre', 'user__fecha_nacimiento',
                'user__domicilio', 'user__ciudad', 'user__afp', 'user__salud', 'user__nivel_estudio',
                'user__telefono', 'user__nacionalidad', 'requerimiento__nombre',  'referido',
                'requerimiento__areacargo', 'requerimiento__centro_costo', 'requerimiento__cliente__razon_social',
                'requerimiento__cliente__rut', 'requerimiento__planta__nombre', 'requerimiento__planta__region',
                'requerimiento__planta__ciudad', 'requerimiento__planta__direccion',
                'requerimiento__planta__gratificacion', 'user__planta__nombre').order_by('user__planta')

        context = super().get_context_data(**kwargs)
    #     context['title'] = 'Listado de Contratos'
    #     context['list_url'] = reverse_lazy('users:<int:user_cliente>/create_cliente')
    #     context['update_url'] = reverse_lazy('utils:update_cliente')
    #     context['cliente'] = cliente
    #     context['entity'] = 'Contratos'
        context['datos'] = RequerimientoTrabajador.objects.filter(pk=requerimiento_trabajador_id).values(
                'user__first_name', 'user__last_name', 'user__rut','user__estado_civil__nombre',
                'user__fecha_nacimiento', 'user__domicilio', 'user__ciudad__nombre', 'user__afp__nombre',
                'user__salud__nombre',
                'user__nivel_estudio__nombre', 'user__telefono', 'user__nacionalidad__nombre', 'requerimiento__nombre',
                'referido', 'area_cargo__area__nombre', 'area_cargo__cargo__nombre', 'requerimiento__centro_costo', 'requerimiento__cliente__razon_social',
                'requerimiento__cliente__rut', 'requerimiento__codigo', 'requerimiento__planta__nombre',
                'requerimiento__planta__region__nombre', 'requerimiento__planta__provincia__nombre',
                'requerimiento__planta__ciudad__nombre', 'requerimiento__planta__direccion',
                'requerimiento__planta__gratificacion__nombre').order_by('user__rut')
    #     context['cliente_id'] = requerimiento_trabajador_id
        context['form3'] = RequeriTrabajadorForm(instance=requer_user, user=trabaj)
        context['form1'] = CrearContratoForm(instance=requer_user)
        return context


class ContratosBonoView(TemplateView):
    """ContratosBono List
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
                for i in ContratosBono.objects.filter(cliente=cliente_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class ContratoMis(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(ContratoMis, self).get_context_data(**kwargs)
        # Obtengo las plantas del Usuario
        plantas = self.request.user.planta.all()
        # Obtengo los ficheros de las plantas a las que pertenece el usuario
        context['ficheros'] = Fichero.objects.filter(
            plantas__in=plantas, status=True, created_by_id=self.request.user
        ).distinct()
        # Obtengo los contratos del usuario si no es administrador.
        if self.request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos']).exists():
            context['contratos'] = Contrato.objects.filter(
                created_by_id=self.request.user).order_by('modified')
        else:
            # Obtengo todos los contratos por firmar de todas las plantas a las
            # que pertenece el usuario.
            context['contratos'] = Contrato.objects.filter(
                usuario__planta__in=plantas, estado=Contrato.POR_FIRMAR, created_by_id=self.request.user)
            context['result'] = Contrato.objects.values(
                'usuario__planta__nombre').order_by('usuario__planta').annotate(count=Count(estado=Contrato.FIRMADO_TRABAJADOR))

        return context


class ContratoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Contrato
    template_name = "contratos/contrato_detail.html"
    context_object_name = "contrato"

    permission_required = 'contratos.view_contrato'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(ContratoDetailView, self).get_context_data(**kwargs)
        # Solo el administrador puede ver el contrato de otro usuario.
        if not self.request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT', ]).exists():
            if not self.object.usuario == self.request.user:
                raise Http404

        # Obtengo todos los documentos del contrato
        documentos = DocumentosContrato.objects.filter(contrato=self.object.id)
        context['documentos'] = documentos

        return context


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class ContratoFirmarView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    slug_url_kwarg = "id"
    slug_field = "id"
    model = Contrato
    template_name = 'registration/password_reset_done.html'
    title = _('Password reset sent')
    template_name = "contratos/contrato_firm.html"
    context_object_name = "contrato"

    permission_required = 'contratos.view_contrato'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(ContratoFirmarView, self).get_context_data(**kwargs)
        # Solo el administrador puede ver el contrato de otro usuario.
        if not self.request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT', ]).exists():
            if not self.object.usuario == self.request.user:
                raise Http404

        # Obtengo todos los documentos del contrato
        documentos = DocumentosContrato.objects.filter(contrato=self.object.id)
        context['documentos'] = documentos

        return context


class generar_firma_contrato(PermissionRequiredMixin, PasswordContextMixin):
        email_template_name = 'emails/contrat_firm_token.html'
        extra_email_context = None
        form_class = PasswordResetForm
        from_email = None
        # from_email = mel@yopmail.com
        html_email_template_name = None
        subject_template_name = 'emails/password_reset_subject.txt'
        success_url = reverse_lazy('password_reset_done')
        template_name = 'emails/contrat_firm_token.html'
        title = _('Password reset')
        token_generator = default_token_generator

        @method_decorator(csrf_protect)
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)

        def form_valid(self, form):
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            form.save(**opts)
            return super().form_valid(form)


        INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

        def generar_firma_contrato(request, contrato_id, template_name='contratos/users_firma_contrato.html'):
            data = dict()
            # Obtengo el usuario
            contrato = get_object_or_404(Contrato, pk=contrato_id)
            print (contrato_id)
            uidb64 = "1s72q4rgru5hyt6fyrjhvc8y1a73piq6"
            token = "oN8ZslfdNk6n6sjUKo63roxbVdfeRHGQthkT48CjlTB57IPj2tn1Ga6d7VRMOGlF"

            if request.method == 'POST':
                print (contrato_id)

            else:
                data['form_is_valid'] = False

            context = {'contrato': contrato, }
            data['html_form'] = render_to_string(
                template_name,
                context,
                request=request
            )
            return JsonResponse(data)


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/contrat_firm_token.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_done.html'
    title = _('Password reset sent')
