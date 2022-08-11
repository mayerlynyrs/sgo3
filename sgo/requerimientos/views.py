from asyncio.windows_events import NULL
from queue import Empty
from django.shortcuts import render

# Create your views here.
"""Requerimientos  Views."""


import json
# Django
import os
import pythoncom
import win32com.client
from docx2pdf import convert
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.conf import settings
from docxtpl import DocxTemplate
from django.db.models import Q, ProtectedError
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.conf import settings
# Model
from requerimientos.models import Requerimiento, AreaCargo, RequerimientoTrabajador, PuestaDisposicion as AnexoPuestaDisposicion, Adendum
from clientes.models import Negocio, Planta
from utils.models import PuestaDisposicion, Gratificacion
from contratos.models import Plantilla
from users.models import User
from epps.models import Convenio, ConvenioRequerimiento, ConvenioRequerTrabajador, AsignacionTrabajador
from examenes.models import Requerimiento as RequerimientoExam
# Form
from requerimientos.forms import RequerimientoCreateForm, ACRForm, RequeriTrabajadorForm, ConvenioTrabajadorForm, AdendumForm
from epps.forms import ConvenioRequerForm, AsignacionTrabajadorForm
from requerimientos.numero_letras import numero_a_letras, numero_a_moneda

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
            requerimiento.fecha_adendum = request.POST['fecha_termino']
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
@permission_required('requerimientos.change_requerimiento', raise_exception=True)
# def adendum_requerimiento(request, requerimiento_id):
#     # data = dict()

#     if request.method == 'POST':

#         form = AdendumForm(request.POST or None)
#     else:
#         form = AdendumForm()

    
#     requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)

#     return render(
#         request=request,
#         template_name='requerimientos/adendum_create.html',
#         context={
#             'requerimiento': requerimiento,
#             'form': form
#         })

    # context = {'requerimiento': requerimiento, }
    # data['html_form'] = render_to_string(
    #     template_name,
    #     context,
    #     request=request,
    # )
    # return JsonResponse(data)    ###


def adendum_requerimiento(request, requerimiento_id, template_name='requerimientos/adendum_create.html'):
    data = dict()
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)

    if request.method == 'POST':

        form = AdendumForm(request.POST or None)

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
        form = AdendumForm(instance=requerimiento,)

    print('requerimiento_id', requerimiento_id)


    # ft_ad = Adendum.objects.values_list('fecha_termino', flat=True).get(requerimiento=requerimiento_id)
    # print('ft_ad', ft_ad)
    # ft_adm = get_object_or_404(Adendum, requerimiento=requerimiento_id)
    # print('ft_adm (get_object_or_404)', ft_adm)
    ft_re = requerimiento.fecha_termino
    print('ft_re', ft_re)

    if not Adendum.objects.filter(requerimiento=requerimiento_id).exists():
        print('no tiene adendum')
        fi_ad = ft_re
        print('fi_ad', fi_ad)
        # print('fecha_termino_adendum es vacia')
    #     fi_ad = ft_re
    # elif ft_ad == ft_re:
    #     print('fecha_termino_adendum es mayor a fecha_termino_requerimiento')
    else:
        # fi_ad = ft_ad
        # print('fecha_termino_adendum es mayor a fecha_termino_requerimiento')
        # print('fecha_inicio_adendum es', fi_ad)
        print('tiene adendum')
        fi_ad = Adendum.objects.filter(requerimiento=requerimiento_id).latest('fecha_termino')
        # fi_ad = Adendum.objects.values_list('fecha_termino', flat=True).get(requerimiento=requerimiento_id)
        print('fi_ad', fi_ad)


    # ft_ad = get_object_or_404(Adendum, requerimiento=requerimiento_id)
    # # fecha_termino_adendum = ft_ad)
    # print('ft_ad', ft_ad)
    # ft_re = requerimiento.fecha_termino
    # # fecha_inicio_adendum = fecha_termino_requerim... == fi_ad
    # print('ft_re', ft_re)
    
    # if date.fromisoformat(str(ft_ad)) > ft_re:
    #     print('mayor')
    # else:
    #     print('menor')


    context={
        'requerimiento': requerimiento,
        'descripcion': requerimiento.descripcion,
        'fecha_inicio': requerimiento.fecha_inicio,
        # Fecha de Término del Requerimiento es la Fecha de Inicio del Adendum
        'fecha_termino': fi_ad,
        'causal': requerimiento.causal,
        'id': requerimiento_id,
        'ad_list': Adendum.objects.filter(requerimiento_id=requerimiento_id, status=True),
        'form': AdendumForm
    }
    
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)

    # return render(
    #     request=request,
    #     template_name='requerimientos/adendum_create.html',


@login_required
@permission_required('requerimientos.add_requerimiento', raise_exception=True)
def create_adendum(request):
    if request.method == 'POST':

        adendum_form = AdendumForm(data=request.POST)
        print(request.POST)
        print('adendum_form', adendum_form)
        # print('AdendumForm', AdendumForm)

        if adendum_form.is_valid():
            ad = adendum_form.save(commit=False)
            if request.POST['fi_ad'] == "":
                ad.fecha_inicio = request.POST['ft_req']
            else:
                ad.fecha_inicio = request.POST['fi_ad']
            ad.requerimiento_id = request.POST['requerimiento_id']
            ad.status = True
            ad.save()
            ad = adendum_form.save()

            messages.success(request, 'Adendum Creado Exitosamente')
            return redirect('requerimientos:list')
            # return redirect('utils:create_cliente', requerimiento_id=requerimiento.id)
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        adendum_form = AdendumForm()
    
    return redirect('requerimientos:list')
    # return render(request, 'requerimientos/requerimiento_create.html', {
    #     'form': adendum_form,
    # })


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
            elif action == 'convenio_add':
                conv_req = ConvenioRequerimiento()
                convenio = Convenio.objects.get(pk=request.POST['convenio'])
                area_cargo = AreaCargo.objects.get(pk=request.POST['area_cargo'])
                conv_req.convenio_id = request.POST['convenio']
                conv_req.area_cargo_id = request.POST['area_cargo']
                conv_req.valor_total = convenio.valor * area_cargo.cantidad
                conv_req.requerimiento_id = requerimiento_id
                conv_req.save()
            elif action == 'convenio_edit':
                conv_req = ConvenioRequerimiento.objects.get(pk=request.POST['id'])
                convenio = Convenio.objects.get(pk=request.POST['convenio'])
                area_cargo = AreaCargo.objects.get(pk=request.POST['area_cargo'])
                conv_req.convenio_id = request.POST['convenio']
                conv_req.area_cargo_id = request.POST['area_cargo']
                conv_req.valor_total = convenio.valor * area_cargo.cantidad
                conv_req.requerimiento_id = requerimiento_id
                conv_req.save()
            elif action == 'convenio_delete':
                conv_req = ConvenioRequerimiento.objects.get(pk=request.POST['id'])
                conv_req.status = False
                conv_req.save()
            # Confirmar = 1
            elif action == '1':
                try:
                    consulta = ConvenioRequerTrabajador.objects.values_list('id', flat=True).get(requerimiento_id=request.POST['requerimiento_id'],area_cargo_id=request.POST['area_cargo_id'],trabajador_id=request.POST['trabajador_id'])
                except ConvenioRequerTrabajador.DoesNotExist:
                    consulta = None
                # Si, consulta es igual a none, crea el registro
                if consulta == None:
                    crt = ConvenioRequerTrabajador()
                    crt.requerimiento_id = requerimiento_id
                    crt.convenio_id = request.POST['convenio_id']
                    crt.area_cargo_id = request.POST['area_cargo_id']
                    crt.trabajador_id = request.POST['trabajador_id']
                    crt.estado = True
                    crt.save()
                # Si no, modifica el registro
                else:
                    crt = ConvenioRequerTrabajador.objects.get(pk=consulta)
                    crt.requerimiento_id = requerimiento_id
                    crt.convenio_id = request.POST['convenio_id']
                    crt.area_cargo_id = request.POST['area_cargo_id']
                    crt.trabajador_id = request.POST['trabajador_id']
                    crt.estado = True
                    crt.save()
            # Anular = 2
            elif action == '2':
                try:
                    consulta = ConvenioRequerTrabajador.objects.values_list('id', flat=True).get(requerimiento_id=request.POST['requerimiento_id'],area_cargo_id=request.POST['area_cargo_id'],trabajador_id=request.POST['trabajador_id'])
                except ConvenioRequerTrabajador.DoesNotExist:
                    consulta = None
                # Si, consulta es igual a none, crea el registro
                if consulta == None:
                    crt = ConvenioRequerTrabajador()
                    crt.requerimiento_id = requerimiento_id
                    crt.convenio_id = request.POST['convenio_id']
                    crt.area_cargo_id = request.POST['area_cargo_id']
                    crt.trabajador_id = request.POST['trabajador_id']
                    crt.estado = False
                    crt.save()
                # Si no, modifica el registro
                else:
                    crt = ConvenioRequerTrabajador.objects.get(pk=consulta)
                    crt.requerimiento_id = requerimiento_id
                    crt.convenio_id = request.POST['convenio_id']
                    crt.area_cargo_id = request.POST['area_cargo_id']
                    crt.trabajador_id = request.POST['trabajador_id']
                    crt.estado = False
                    crt.save()
            elif action == 'requeri_trab_add':
                trabaj = RequerimientoTrabajador()
                if "referido" in request.POST:
                    estado = True
                    trabaj.referido =  estado
                else:
                    estado = False
                    trabaj.referido =  estado
                trabaj.descripcion = request.POST['descripcion']
                trabaj.tipo_id = request.POST['tipo']
                trabaj.pension = request.POST['pension']
                trabaj.area_cargo_id = request.POST['area_cargo_id']
                trabaj.trabajador_id = request.POST['trabajador']
                trabaj.jefe_area_id = request.POST['jefe_area']
                trabaj.id_requerimiento_trabajador = str(requerimiento_id)+str(request.POST['trabajador'])
                trabaj.requerimiento_id = requerimiento_id
                trabaj.save()
            elif action == 'requeri_trab_edit':
                trabaj = RequerimientoTrabajador.objects.get(pk=request.POST['id'])
                if "referido" in request.POST:
                    estado = True
                    trabaj.referido =  estado
                else:
                    estado = False
                    trabaj.referido =  estado
                trabaj.descripcion = request.POST['descripcion']
                trabaj.tipo_id = request.POST['tipo']
                trabaj.pension = request.POST['pension']
                trabaj.area_cargo_id = request.POST['area_cargo']
                trabaj.trabajador_id = request.POST['trabajador']
                trabaj.jefe_area_id = request.POST['jefe_area']
                # trabaj.area_cargo_id = 10
                trabaj.id_requerimiento_trabajador = str(requerimiento_id)+request.POST['trabajador']
                trabaj.requerimiento_id = requerimiento_id
                trabaj.save()
            elif action == 'requeri_trab_delete':
                trabaj = RequerimientoTrabajador.objects.get(pk=request.POST['id'])
                trabaj.status = False
                trabaj.save()
            elif action == 'exam_rev_add':
                req_trab = RequerimientoTrabajador.objects.values_list('id', 'trabajador', 'requerimiento__planta', 'requerimiento__planta__bateria', 'requerimiento__planta__psicologico', 'requerimiento__planta__hal2').filter(requerimiento=requerimiento_id)
                # print(req_trab)
                for a in req_trab:
                    exa_req = RequerimientoExam()
                    # print('a',a[1])
                    exa_req.estado = 'E'                            # Enviado
                    exa_req.resultado = None
                    exa_req.requerimiento_trabajador_id = a[0]      # a.id
                    if a[3] != None:
                        exa_req.bateria_id = a[3]
                    if a[4] == True:
                        exa_req.psicologico = a[4]
                    if a[5] == True:
                        exa_req.hal2 = a[5]
                    exa_req.trabajador_id = a[1]                   # a.trabajador
                    exa_req.planta_id = a[2]                       # a.requerimiento__planta
                    exa_req.save()
            elif action == 'epp_trab_add':
                asignar = AsignacionTrabajador()
                if "tipo_asignacion" in request.POST:
                    estado = True
                    asignar.tipo_asignacion =  estado
                else:
                    estado = False
                    asignar.tipo_asignacion =  estado
                asignar.insumo_id = request.POST['insumo']
                asignar.cantidad = request.POST['cantidad']
                asignar.area_cargo_id = request.POST['area_cargo_id']
                asignar.trabajador_id = request.POST['trabajador_id']
                asignar.requerimiento_id = requerimiento_id
                asignar.save()
            # Anular = 3
            elif action == '3':
                borrar = AsignacionTrabajador.objects.get(pk=request.POST['id'])
                borrar.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, requerimiento_id, **kwargs):

        requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)
        # Convenio de la Planta
        convenio_plant = Convenio.objects.filter(planta_id=requerimiento.planta)
        # Áreas - Cargos del Requerimiento
        ac = AreaCargo.objects.filter(requerimiento_id=requerimiento_id)
        # Trabajadores del Áreas - Cargos de dicho Requerimiento
        req_conv_trab = RequerimientoTrabajador.objects.all()
        # (cantidad) Trabajadores en el Área(s) y Cargo(s) del Requerimiento
        pk = requerimiento_id
        quantity = RequerimientoTrabajador.objects.filter(requerimiento_id=pk).count()

        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('users:<int:user_cliente>/create_cliente')
        context['update_url'] = reverse_lazy('requerimientos:update')
        context['entity'] = 'Requerimientos'
        context['requerimiento_id'] = requerimiento_id
        context['form'] = RequerimientoCreateForm(instance=requerimiento)
        context['form2'] = ACRForm(instance=requerimiento,
                                   areas=requerimiento.cliente.area.all(),
                                   cargos=requerimiento.cliente.cargo.all(),
                                   cantidad=quantity
                                   )
        context['form3'] = ConvenioRequerForm(instance=requerimiento, convenio=convenio_plant, area_cargo=ac)
        context['form4'] = RequeriTrabajadorForm(instance=requerimiento, area_cargo=ac)
        context['form5'] = AsignacionTrabajadorForm(instance=requerimiento)
        # context['req_trab'] = RequerimientoTrabajador(instance=requerimiento, pk=requerimiento_id)
        context['trabajadores'] = RequerimientoTrabajador.objects.filter(requerimiento_id=requerimiento_id, status=True)
        # context['a_c_trab'] = RequerimientoTrabajador.objects.values_list('area_cargo', flat=True).get(requerimiento_id=requerimiento_id, status=True)
        areas_cargos = RequerimientoTrabajador.objects.values('area_cargo', ).filter(requerimiento_id=requerimiento_id, status=True)
        ac_req = []
        for i in areas_cargos:
            ac_req.append(i)
            context['a_c_trab'] = ac_req
        # context['form5'] = ConvenioTrabajadorForm(instance=requerimiento, trabaj_conve=req_conv_trab)
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


class RequirementConvenioView(TemplateView):
    """RequirementConvenio List
    Vista para listar todos los convenios del requiremento segun las plantas
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
                for i in ConvenioRequerimiento.objects.filter(requerimiento=requerimiento_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class RequirementTrabajadorView(TemplateView):
    """RequirementTrabajador List
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
            if action == 'searchdata4':
                data = []
                # for i in RequerimientoTrabajador.objects.filter(area_cargo=area_cargo_id, status=True):
                for i in RequerimientoTrabajador.objects.filter(requerimiento=requerimiento_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class ConveniotrabajadorView(TemplateView):
    """Conveniotrabajador List
    Vista para listar todos los convenios del requerimiento y sus trabajadores
    relacionados.
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
            if action == 'searchdata6':
                data = []
                for i in RequerimientoTrabajador.objects.filter(area_cargo_id=area_cargo_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class AsignartrabajadorView(TemplateView):
    """Asignartrabajador List
    Vista para listar todas las asignaciones del requerimiento y sus trabajadores
    relacionados.
    """
    template_name = 'requerimientos/create_requerimiento.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, trabajador_id, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata8':
                data = []
                for i in AsignacionTrabajador.objects.filter(trabajador=trabajador_id, status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


def a_puesta_disposicion(request, requerimiento_id):

    # Trae el id de la planta del Requerimiento
    plant_template = Requerimiento.objects.values_list('planta', flat=True).get(pk=requerimiento_id, status=True)
    # Trae la plantilla que tiene la planta
    formato = Plantilla.objects.values_list('archivo', flat=True).get(plantas=plant_template, tipo_id=3)

    # if formato == '':
    #     print('sin planilla')
    #     messages.warning(request, 'La planta no posee Plantilla ')
    #     return redirect('requerimientos:list')
    # else:
    #     print('con planilla')
    #     print(formato)

    # requer = Requerimiento.objects.filter(pk=requerimiento_id).values('codigo', 'fecha_solicitud', 'planta__ciudad__nombre',
    #                                         'planta__direccion_gerente', 'cliente__razon_social', 'cliente__rut',
    #                                         'planta__nombre', 'planta__nombre_gerente', 'planta__rut', 'causal__nombre',
    #                                         'causal__descripcion', 'descripcion', 'fecha_inicio', 'fecha_termino')
    # print('requer', requer)

    
    # Fecha actual que se utiliza en el documento Puesta Disposición (codigo/año_actual)
    now = datetime.now()

    # cargos = AreaCargo.objects.filter(requerimiento=requerimiento_id).values('cargo__nombre')
    razon_social = Requerimiento.objects.values_list('cliente__razon_social', flat=True).get(pk=requerimiento_id, status=True)

    # Cargo(s) del requerimiento
    acr = AreaCargo.objects.values('cargo__nombre', 'cantidad', 'area__nombre', ).filter(requerimiento=requerimiento_id, status=True)
    acreq = []
    for i in acr:
        acreq.append(i)
        # print('acreq', acreq)

    # # Cantidad de personas del requerimiento
    # cantidades = AreaCargo.objects.values_list('cantidad', flat=True).filter(requerimiento=requerimiento_id)
    # numero = []
    # for i in cantidades:
    #     numero.append(i)

    fecha_inicio = Requerimiento.objects.values_list('fecha_inicio', flat=True).get(pk=requerimiento_id, status=True)
    fecha_termino = Requerimiento.objects.values_list('fecha_termino', flat=True).get(pk=requerimiento_id, status=True)
    # Total de días del requerimiento
    duracion = (fecha_termino - fecha_inicio).days
    # print('totalDiasRequerimiento', duracion)

    for e in PuestaDisposicion.objects.all():
        gratificacion = (e.gratificacion)
        # print('gratificacion', gratificacion)

    for e in PuestaDisposicion.objects.all():
        seguro_cesantia = (e.seguro_cesantia)

    for e in PuestaDisposicion.objects.all():
        seguro_invalidez = (e.seguro_invalidez)

    for e in PuestaDisposicion.objects.all():
        seguro_vida = (e.seguro_vida)

    for e in PuestaDisposicion.objects.all():
        mutual = (e.mutual)

    # valor_aprox del requerimiento
    valor_aprox = AreaCargo.objects.values_list('valor_aprox', flat=True).filter(requerimiento=requerimiento_id, status=True)
    # print('valor_aprox', valor_aprox)
    # doc = DocxTemplate("sgo/media/"+formato)
    
    # Fecha de Inicio en Palabras
    if fecha_inicio.month == 1:
        mes = 'Enero'
    elif fecha_inicio.month == 2:
        mes = 'Febrero'
    elif fecha_inicio.month == 3:
        mes = 'Marzo'
    elif fecha_inicio.month == 4:
        mes = 'Abril'
    elif fecha_inicio.month == 5:
        mes = 'Mayo'
    elif fecha_inicio.month == 6:
        mes = 'Junio'
    elif fecha_inicio.month == 7:
        mes = 'Julio'
    elif fecha_inicio.month == 8:
        mes = 'Agosto'
    elif fecha_inicio.month == 9:
        mes = 'Septiembre'
    elif fecha_inicio.month == 10:
        mes = 'Octubre'
    elif fecha_inicio.month == 11:
        mes = 'Noviembre'
    elif fecha_inicio.month == 12:
        mes = 'Diciembre'
    fechainicio_palabras = str(fecha_inicio.day) + ' de ' + mes + ' de ' + str(fecha_inicio.year)
    
    # Fecha Término en Palabras 
    if fecha_termino.month == 1:
        mes = 'Enero'
    elif fecha_termino.month == 2:
        mes = 'Febrero'
    elif fecha_termino.month == 3:
        mes = 'Marzo'
    elif fecha_termino.month == 4:
        mes = 'Abril'
    elif fecha_termino.month == 5:
        mes = 'Mayo'
    elif fecha_termino.month == 6:
        mes = 'Junio'
    elif fecha_termino.month == 7:
        mes = 'Julio'
    elif fecha_termino.month == 8:
        mes = 'Agosto'
    elif fecha_termino.month == 9:
        mes = 'Septiembre'
    elif fecha_termino.month == 10:
        mes = 'Octubre'
    elif fecha_termino.month == 11:
        mes = 'Noviembre'
    elif fecha_termino.month == 12:
        mes = 'Diciembre'
    fechatermino_palabras = str(fecha_termino.day) + ' de ' + mes + ' de ' + str(fecha_termino.year)
    codigo= Requerimiento.objects.values_list('codigo', flat=True).get(pk=requerimiento_id, status=True)+'/'+str(now.year)
    motivo = Requerimiento.objects.values_list('descripcion', flat=True).get(pk=requerimiento_id, status=True)

    # valor_aprox = []
    # if not valor_aprox:
    #     print('sin total')
    #     messages.warning(request, 'El requerimiento no posee Área-Cargo')
    #     return redirect('requerimientos:list')
    # else:
    #     print('con total')
    #     print(valor_aprox)
    
    k = 0
    sueldo_base_gratif = 0
    sueldototal = []
    subtotal_pd = 0
    valortotal = []
    trabajadores = AreaCargo.objects.values_list('cantidad', flat=True).filter(requerimiento=requerimiento_id, status=True)
    # cantidad_trabajadores = 0
    cargos = AreaCargo.objects.values_list('cargo', flat=True).filter(requerimiento=requerimiento_id, status=True)
    # cargo = 0
    trabajador = []
    cargo = []
    for sueldo_base in valor_aprox:
        # print('sueldo_base', sueldo_base)
        sueldototal.append((((sueldo_base+gratificacion)/30)*duracion))
        sueldo_base_gratif=round((((sueldo_base+gratificacion)/30)*duracion))
        valortotal.append(round(sueldototal[k]+((sueldototal[k]*mutual)/100)+((sueldototal[k] *seguro_cesantia)/100)+(sueldototal[k] *seguro_invalidez)+((seguro_vida/30)*duracion)))
        subtotal_pd=round(sueldototal[k]+((sueldototal[k]*mutual)/100)+((sueldototal[k] *seguro_cesantia)/100)+(sueldototal[k] *seguro_invalidez)+((seguro_vida/30)*duracion))
        total = round(sum(valortotal))
        totalpalabras = numero_a_letras(total)
    for trabajador, cargo in zip(trabajadores, cargos):
        print('valortotal', total)

        requer = AnexoPuestaDisposicion()
        requer.codigo_pd = codigo
        requer.fecha_pd = now
        requer.motivo_pd = motivo
        requer.fecha_inicio = fecha_inicio
        requer.fechainicio_text = fechainicio_palabras
        requer.fecha_termino = fecha_termino
        requer.fechatermino_text = fechatermino_palabras
        requer.dias_pd = duracion
        requer.dias_totales = duracion
        requer.sueldo_base = sueldo_base
        requer.sueldo_base_gratif = sueldo_base_gratif
        requer.subtotal_pd = subtotal_pd
        requer.valor_total_pd = total
        requer.total_redondeado = total
        requer.total_redondeado_text = totalpalabras
        requer.cantidad_trabajadores = trabajador
        requer.cargo_id = cargo
        requer.causal_id = 1
        requer.requerimiento_id = requerimiento_id
        requer.status = True
        requer.save()
        k = k + 1


        # valor = [248886.4602, 248886.4602, 83137.20000000001]
        # print("***valor_total['248886.4602', '248886.4602', '83137.20000000001']***", valor_total[0:1] = [float(0)])
        
        

    # Documento word a trabajar, segun el requerimiento
    doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT + '/' + formato))

    context = { 'codigo': codigo,
                'fechaHoy': Requerimiento.objects.values_list('fecha_solicitud', flat=True).get(pk=requerimiento_id, status=True),
                'nombreCiudad': Requerimiento.objects.values_list('planta__ciudad__nombre', flat=True).get(pk=requerimiento_id, status=True),
                'domicilioGerente': Requerimiento.objects.values_list('planta__direccion_gerente', flat=True).get(pk=requerimiento_id, status=True),
                'razonSocial': razon_social,
                'razonSocialMayus': razon_social.upper(),
                'rut': Requerimiento.objects.values_list('cliente__rut', flat=True).get(pk=requerimiento_id, status=True),
                'nombrePlanta': Requerimiento.objects.values_list('planta__nombre', flat=True).get(pk=requerimiento_id, status=True),
                'nombreGerente': Requerimiento.objects.values_list('planta__nombre_gerente', flat=True).get(pk=requerimiento_id, status=True),
                'rutGerente': Requerimiento.objects.values_list('planta__rut', flat=True).get(pk=requerimiento_id, status=True),
                'letraCausal': Requerimiento.objects.values_list('causal__nombre', flat=True).get(pk=requerimiento_id, status=True),
                'descripcionCausal': Requerimiento.objects.values_list('causal__descripcion', flat=True).get(pk=requerimiento_id, status=True),
                'motivo': motivo,
                'articuloQuinto': Requerimiento.objects.values_list('codigo', flat=True).get(pk=requerimiento_id, status=True),
                'totalDiasRequerimiento': duracion,
                'fechainicioreq': fechainicio_palabras,
                'fechaterminoreq': fecha_termino,
                'cargo': acreq,    
                # 'numero': numero,
                'valor': valortotal,
                'totalredondeado': total,
                'totalredondeadopalabras': totalpalabras,
                }

    doc.render(context)
    # exit()
    # Obtengo el usuario
    usuario = get_object_or_404(User, pk=1)
    # Obtengo todas las negocios a las que pertenece el usuario.
    plantas = usuario.planta.all()
    # Obtengo el set de contrato de la primera negocio relacionada.
    plantillas_attr = list()
    plantillas = Plantilla.objects.filter(activo=True, plantas=plantas[0].id)
    # Obtengo los atributos de cada plantilla
    for p in plantillas:
        plantillas_attr.extend(list(p.atributos))

    path = os.path.join(settings.MEDIA_ROOT + '/plantillas/')
    doc.save(path + '/PuestaDisposicion#' + str(requerimiento_id) + '.docx')
    win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
    # convert("PuestaDisposicion#1.docx")
    convert(path + "PuestaDisposicion#" + str(requerimiento_id) + ".docx", path + "PuestaDisposicion#" + str(requerimiento_id) + ".pdf")

    # Elimino el documento word.
    os.remove(path + 'PuestaDisposicion#' + str(requerimiento_id) + '.docx')

    messages.success(request, 'Anexo Puesta Dispocisión Exitosamente')

    requer = Requerimiento.objects.get(pk=requerimiento_id)
    requer.bloqueo = True
    requer.requerimiento_id = requerimiento_id
    requer.save()

    messages.success(request, 'Requerimiento Bloqueado')
    return redirect('requerimientos:list')


def descargar_adendum(request, adendum_id):

    # Trae el id del Requerimiento en el adendum
    requerimiento_id = Adendum.objects.values_list('requerimiento_id', flat=True).get(pk=adendum_id, status=True)
    print('requerimiento_id del adendum', requerimiento_id)

    # Trae el id de la planta del Requerimiento
    plant_template = Requerimiento.objects.values_list('planta', flat=True).get(pk=requerimiento_id, status=True)
    # Trae la plantilla que tiene la planta
    formato = Plantilla.objects.values_list('archivo', flat=True).get(plantas=plant_template, tipo_id=4)

    # Fecha actual que se utiliza en el documento Puesta Disposición (codigo/año_actual)
    now = datetime.now()

    # cargos = AreaCargo.objects.filter(requerimiento=requerimiento_id).values('cargo__nombre')
    razon_social = Requerimiento.objects.values_list('cliente__razon_social', flat=True).get(pk=requerimiento_id, status=True)

    # Cargo(s) del requerimiento
    acr = AreaCargo.objects.values('cargo__nombre', 'cantidad', 'area__nombre', ).filter(requerimiento=requerimiento_id, status=True)
    acreq = []
    for i in acr:
        acreq.append(i)
        # print('acreq', acreq)

    fecha_inicio = Requerimiento.objects.values_list('fecha_inicio', flat=True).get(pk=requerimiento_id, status=True)
    fecha_termino = Requerimiento.objects.values_list('fecha_termino', flat=True).get(pk=requerimiento_id, status=True)
    # Total de días del requerimiento
    duracion = (fecha_termino - fecha_inicio).days
    # print('totalDiasRequerimiento', duracion)

    for e in PuestaDisposicion.objects.all():
        gratificacion = (e.gratificacion)
        # print('gratificacion', gratificacion)

    for e in PuestaDisposicion.objects.all():
        seguro_cesantia = (e.seguro_cesantia)

    for e in PuestaDisposicion.objects.all():
        seguro_invalidez = (e.seguro_invalidez)

    for e in PuestaDisposicion.objects.all():
        seguro_vida = (e.seguro_vida)

    for e in PuestaDisposicion.objects.all():
        mutual = (e.mutual)

    # valor_aprox del requerimiento
    valor_aprox = AreaCargo.objects.values_list('valor_aprox', flat=True).filter(requerimiento=requerimiento_id, status=True)
    # print('valor_aprox', valor_aprox)
    
    k = 0
    sueldototal = []
    valortotal = []
    for sueldo_base in valor_aprox:
        # print('sueldo_base', sueldo_base)
        sueldototal.append((((sueldo_base+gratificacion)/30)*duracion))
        valortotal.append(round(sueldototal[k]+((sueldototal[k]*mutual)/100)+((sueldototal[k] *seguro_cesantia)/100)+(sueldototal[k] *seguro_invalidez)+((seguro_vida/30)*duracion)))
        total = round(sum(valortotal))
        totalpalabras = numero_a_letras(total)
        print('valortotal', total)
        k = k + 1

    # Documento word a trabajar, segun el requerimiento
    doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT + '/' + formato))
    # doc = DocxTemplate("sgo/media/"+formato)
    
    # Fecha de Inicio en Palabras
    if fecha_inicio.month == 1:
        mes = 'Enero'
    elif fecha_inicio.month == 2:
        mes = 'Febrero'
    elif fecha_inicio.month == 3:
        mes = 'Marzo'
    elif fecha_inicio.month == 4:
        mes = 'Abril'
    elif fecha_inicio.month == 5:
        mes = 'Mayo'
    elif fecha_inicio.month == 6:
        mes = 'Junio'
    elif fecha_inicio.month == 7:
        mes = 'Julio'
    elif fecha_inicio.month == 8:
        mes = 'Agosto'
    elif fecha_inicio.month == 9:
        mes = 'Septiembre'
    elif fecha_inicio.month == 10:
        mes = 'Octubre'
    elif fecha_inicio.month == 11:
        mes = 'Noviembre'
    elif fecha_inicio.month == 12:
        mes = 'Diciembre'
    fechainicio_palabras = str(fecha_inicio.day) + ' de ' + mes + ' de ' + str(fecha_inicio.year)
    
    # Fecha Término en Palabras 
    if fecha_termino.month == 1:
        mes = 'Enero'
    elif fecha_termino.month == 2:
        mes = 'Febrero'
    elif fecha_termino.month == 3:
        mes = 'Marzo'
    elif fecha_termino.month == 4:
        mes = 'Abril'
    elif fecha_termino.month == 5:
        mes = 'Mayo'
    elif fecha_termino.month == 6:
        mes = 'Junio'
    elif fecha_termino.month == 7:
        mes = 'Julio'
    elif fecha_termino.month == 8:
        mes = 'Agosto'
    elif fecha_termino.month == 9:
        mes = 'Septiembre'
    elif fecha_termino.month == 10:
        mes = 'Octubre'
    elif fecha_termino.month == 11:
        mes = 'Noviembre'
    elif fecha_termino.month == 12:
        mes = 'Diciembre'
    fechatermino_palabras = str(fecha_termino.day) + ' de ' + mes + ' de ' + str(fecha_termino.year)

    context = { 'codigo': Requerimiento.objects.values_list('codigo', flat=True).get(pk=requerimiento_id, status=True) + '-' + str(now.year)+'/AD'+ str(adendum_id),
                'fechaHoy': Requerimiento.objects.values_list('fecha_solicitud', flat=True).get(pk=requerimiento_id, status=True),
                'nombreCiudad': Requerimiento.objects.values_list('planta__ciudad__nombre', flat=True).get(pk=requerimiento_id, status=True),
                'domicilioGerente': Requerimiento.objects.values_list('planta__direccion_gerente', flat=True).get(pk=requerimiento_id, status=True),
                'razonSocial': razon_social,
                'razonSocialMayus': razon_social.upper(),
                'rut': Requerimiento.objects.values_list('cliente__rut', flat=True).get(pk=requerimiento_id, status=True),
                'nombrePlanta': Requerimiento.objects.values_list('planta__nombre', flat=True).get(pk=requerimiento_id, status=True),
                'nombreGerente': Requerimiento.objects.values_list('planta__nombre_gerente', flat=True).get(pk=requerimiento_id, status=True),
                'rutGerente': Requerimiento.objects.values_list('planta__rut', flat=True).get(pk=requerimiento_id, status=True),
                'letraCausal': Requerimiento.objects.values_list('causal__nombre', flat=True).get(pk=requerimiento_id, status=True),
                'descripcionCausal': Requerimiento.objects.values_list('causal__descripcion', flat=True).get(pk=requerimiento_id, status=True),
                'motivo': Requerimiento.objects.values_list('descripcion', flat=True).get(pk=requerimiento_id, status=True),
                'articuloQuinto': Requerimiento.objects.values_list('codigo', flat=True).get(pk=requerimiento_id, status=True),
                'totalDiasRequerimiento': duracion,
                'fechainicioreq': fecha_inicio,
                'fechaterminoreq': fecha_termino,
                'cargo': acreq,    
                # 'numero': numero,
                'valor': valortotal,
                'totalredondeado': total,
                'totalredondeadopalabras': totalpalabras,
                }

    doc.render(context)
    # exit()
    # Obtengo el usuario
    usuario = get_object_or_404(User, pk=request.user.id)
    # Obtengo todas las negocios a las que pertenece el usuario.
    plantas = usuario.planta.all()
    # Obtengo el set de contrato de la primera negocio relacionada.
    plantillas_attr = list()
    plantillas = Plantilla.objects.filter(activo=True, plantas=plantas[0].id)
    # Obtengo los atributos de cada plantilla
    for p in plantillas:
        plantillas_attr.extend(list(p.atributos))

    path = os.path.join(settings.MEDIA_ROOT + '/plantillas/')
    doc.save(path + '/Adendum#' + str(requerimiento_id) + '_' + str(adendum_id) + '.docx')
    win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
    # convert("Adendum#1.docx")
    convert(path + "Adendum#" + str(requerimiento_id) + '_' + str(adendum_id) + ".docx", path + "Adendum#" + str(requerimiento_id) + '_' + str(adendum_id) + ".pdf")

    # Elimino el documento word.
    os.remove(path + 'Adendum#' + str(requerimiento_id) + '_' + str(adendum_id) + '.docx')

    requer = Adendum.objects.get(pk=adendum_id)
    # requer.fecha_inicio = fecha_inicio
    requer.fechainicio_text = fechainicio_palabras
    # requer.fecha_termino = fecha_termino
    requer.fechatermino_text = fechatermino_palabras
    requer.dias_ad = duracion
    requer.dias_totales_ad = duracion
    requer.sueldo_base = sueldo_base
    # requer.sueldo_base_gratif = sueldo_base_gratif
    # requer.subtotal_ad = subtotal_ad
    # requer.valor_total_pd = valortotal
    requer.total_redondeado_ad = total
    requer.total_redondeado_ad_text = totalpalabras
    # requer.requerimiento_id = requerimiento_id
    requer.status = True
    requer.save()

    messages.success(request, 'Adendum Exitosamente')

    # requer = Requerimiento.objects.get(pk=requerimiento_id)
    # requer.bloqueo = True
    # requer.requerimiento_id = requerimiento_id
    # requer.save()

    # messages.success(request, 'Requerimiento Bloqueado')
    return redirect('requerimientos:list')
