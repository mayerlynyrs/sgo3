"""Contratos views."""

from itertools import chain
from asyncio.windows_events import NULL
from cgi import print_form
from multiprocessing import context
from optparse import Values
from queue import Empty
from telnetlib import STATUS
from tkinter import FLAT
from datetime import date, datetime, timedelta
from docx2pdf import convert
from django.core.serializers import serialize
import base64
# Django
import os
import xlwt
from django.http import HttpResponse
import pythoncom
import win32com.client
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q, ProtectedError
from django.forms import NullBooleanField
from django.views.generic import TemplateView
from django.db.models import Count
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from docxtpl import DocxTemplate
from django.core.mail import send_mail
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
from contratos.models import TipoContrato, Contrato, DocumentosContrato, ContratosBono, Anexo, Revision, Baja, FinRequerimiento, ContratosParametrosGen
from requerimientos.models import Requerimiento, RequerimientoTrabajador
from contratos.models import Plantilla
from users.models import User, Trabajador, ValoresDiarioAfp
from clientes.models import Planta
from utils.models import PuestaDisposicion
# Form
from contratos.forms import PuestaDisposicionForm, TipoContratoForm, ContratoForm, ContratoEditarForm, MotivoBajaForm, CompletasForm
from requerimientos.forms import RequeriTrabajadorForm
from requerimientos.numero_letras import numero_a_letras
from requerimientos.fecha_a_palabras import fecha_a_letras
from contratos.finiquito import finiquito
now = datetime.now()


class PuestaDisposicionView(TemplateView):
    template_name = 'contratos/puesta_disposicion.html'

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
                for i in PuestaDisposicion.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                fpd = PuestaDisposicion()
                fpd.nombre = request.POST['nombre'].lower()
                fpd.status = True
                fpd.save()
            elif action == 'edit':
                fpd = PuestaDisposicion.objects.get(pk=request.POST['id'])
                fpd.nombre = request.POST['nombre'].lower()
                fpd.gratificacion = request.POST['gratificacion']
                fpd.seguro_cesantia = request.POST['seguro_cesantia']
                fpd.seguro_invalidez = request.POST['seguro_invalidez']
                fpd.seguro_vida = request.POST['seguro_vida']
                fpd.mutual = request.POST['mutual']
                fpd.save()
            elif action == 'delete':
                fpd = PuestaDisposicion.objects.get(pk=request.POST['id'])
                fpd.status = False
                fpd.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Puesta a Disposición'
        context['list_url'] = reverse_lazy('contratos:puesta_disposicion')
        context['entity'] = 'PuestaDisposicion'
        context['form'] = PuestaDisposicionForm()
        return context


class TipoContratosView(TemplateView):
    template_name = 'contratos/tipo_contratos_list.html'

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
                for i in TipoContrato.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                tipo = TipoContrato()
                tipo.nombre = request.POST['nombre'].lower()
                tipo.status = True
                tipo.save()
            elif action == 'edit':
                tipo = TipoContrato.objects.get(pk=request.POST['id'])
                tipo.nombre = request.POST['nombre'].lower()
                tipo.save()
            elif action == 'delete':
                tipo = TipoContrato.objects.get(pk=request.POST['id'])
                tipo.status = False
                tipo.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipo Contratos'
        context['list_url'] = reverse_lazy('contratos:tipo_contrato')
        context['entity'] = 'TipoContrato'
        context['form'] = TipoContratoForm()
        return context


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
def exportar_excel_contrato(request):

    planta = request.POST.get('planta')
    mes = request.POST.get('mes')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('reporte')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['RUT','APELLIDO PATERNO','APELLIDO MATERNO','PRIMER NOMBRE','SEGUNDO NOMBRE','TELEFONO', 'CELULAR', 'CORREO ELECTRONICO','PAIS (CODIGO)',  'CIUDAD (CODIGO)', 'COMUNA (CODIGO)', 'CALLE (CODIGO)', 'NRO_DIRECCION'
    , 'DETALLE_DIRECCION', 'NACIONALIDAD', 'SEXO (CODIGO)', 'ESTADO_CIVIL (CODIGO)', 'FECHA_NACIMIENTO', 'LUGAR_DE_NACIMIENTO', 'PANTALON', 'CHAQUETA', 'ZAPATO', 'SITUACION (CODIGO)',
'PROFESION (CODIGO)', 'SINDICATO', 'BANCO (CODIGO)', 'CODIGO_OFICINA_PAGO','NRO_CUENTA', 'TIPO_DE_CUENTA_CODIGO', 'FECHA_INI_ACTIVIDAD', 'GRUPO_SANGRE', 'ESTATURA', 'PESO', 'AFP (CODIGO)', 'AFP PACTADO',
'AFP_CONVENIO(CODIGO)', 'AHORRO AFP', 'MONTO JUBILACION', 'N_FUN', 'ISAPRE (CODIGO)', 'ISAPRE PACTADO', 'ISA_CONVENIO(CODIGO)', 'SERV_MEDICO_CARGA_NORMAL', 'SERV_MEDICO_CARGA_ESPECIAL', 'SERV_MEDICO_CARGA_DENTAL',
 'SERV_MEDICO_ADICIONAL', 'SERVM_CONVENIO(CODIGO)', 'INST_APV (CODIGO)' , 'MONTO APV', 'APV_CONVENIO(CODIGO)', 'INST_SEGURO_CESANTIA (CODIGO)' , 'PRESENTADO_POR' , 'RUTA_CURRICULUM', 'OBSERVACIONES', 'RUTA_IMAGEN', 'NIC', 'FECHA_CONTRATO',
 'FECHA_INICIO', 'FECHA_TERMINO', 'CONSORCIO (CODIGO)', 'EMPRESA (CODIGO)', 'OBRA (CODIGO)', 'CENTRO_COSTO (CODIGO)' , 'CARGO (CODIGO)', 'SUELDO_BASE_MES', 'SUELDO_BASE_DIA', 'SUELDO_BASE_HORA', 'QUINCENA', 'LUGAR_PAGO (CODIGO)','DIA_PAGO',
 'LIQUIDO_PACTADO', 'TURNO (CODIGO)', 'CLASIFICACION_TRABAJADOR (CODIGO)', 'ID_PEDIDO', 'HITO (CODIGO)', 'SUPERVISOR', 'ID_TIPO_CONTRATO', 'NIVEL_EDUCACIONAL', 'CAUSAL_CONTRATACION', 'LETRA_CONTRATO', ' TIPO_CONTRATO', 'COLABORADOR_REFERIDO',
 'CODIGO_INTERNO_CC', 'MOTIVO_CONTRATO', 'CUENTA_CONTABLE','ADHERIDO ISAPRE','SEG','ASIG MOV', 'ASIG PERD CAJA', 'NO PAGA SIS', 'FECHA DE PAGO', 'FERIADO PROPORCIONAL', 'A PAGO LIQUIDO'
 ]

    for col_num in range(len(columns)):
        
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()


    rows = Contrato.objects.filter(estado_contrato='AP', planta_id=planta, fecha_inicio__month=mes, status=True).values_list('trabajador__rut', 'trabajador__last_name',  'regimen', 'trabajador__first_name',   'trabajador__telefono', 'trabajador__telefono'
    ,'trabajador__telefono', 'trabajador__email', 'trabajador__domicilio','trabajador__region__id', 'trabajador__ciudad__cod_uny_ciudad',  'trabajador__domicilio','requerimiento_trabajador__requerimiento__areacargo__cargo__nombre', 'trabajador__domicilio', 'trabajador__nacionalidad__nombre', 'trabajador__sexo__nombre', 'trabajador__estado_civil__nombre',
    'trabajador__fecha_nacimiento','trabajador__rut','trabajador__rut','trabajador__rut','trabajador__rut','trabajador__rut', 'requerimiento_trabajador__requerimiento__areacargo__cargo__cod_uny_cargo', 'trabajador__banco__rut', 'trabajador__banco__rut', 'trabajador__banco__codigo','trabajador__cuenta','trabajador__afp__cod_uny_afp','trabajador__afp__cod_uny_afp'
    ,'trabajador__afp__cod_uny_afp','trabajador__afp__cod_uny_afp','trabajador__afp__cod_uny_afp','trabajador__afp__cod_uny_afp','trabajador__salud__cod_uny_salud','trabajador__pacto_uf' ,'trabajador__pacto_uf' ,'trabajador__pacto_uf' ,'trabajador__salud__cod_uny_salud', 'trabajador__pacto_uf','trabajador__pacto_uf','trabajador__rut','trabajador__rut'
    ,'trabajador__rut','trabajador__rut','trabajador__rut','trabajador__rut','trabajador__rut','trabajador__rut' ,'trabajador__afp__cod_uny_afp' ,'trabajador__afp__cod_uny_afp' ,'trabajador__afp__cod_uny_afp' ,'trabajador__afp__cod_uny_afp' ,'trabajador__afp__cod_uny_afp' ,'trabajador__afp__cod_uny_afp' , 'fecha_inicio' , 'fecha_inicio'
    , 'fecha_inicio' , 'fecha_termino' , 'fecha_termino', 'fecha_termino','planta__cliente__cod_uny_cliente', 'planta__cod_uny_planta'
    , 'requerimiento_trabajador__requerimiento__areacargo__cargo__cod_uny_cargo', 'sueldo_base', 'sueldo_base', 'sueldo_base', 'sueldo_base',"planta__cod_uny_planta", "planta__cod_uny_planta", "planta__cod_uny_planta", "horario__cod_uny_horario", "planta__cod_uny_planta", "planta__cod_uny_planta", "planta__cod_uny_planta", "created_by_id__rut", "trabajador__nivel_estudio__cod_uny_estudio"
    , "trabajador__nivel_estudio__cod_uny_estudio", "causal__id", "causal__nombre", "regimen", "requerimiento_trabajador__referido", "requerimiento_trabajador__requerimiento__centro_costo", "requerimiento_trabajador__requerimiento__descripcion", "motivo", "trabajador__salud__id", "trabajador__afp", "motivo" , "motivo" , "motivo", "fecha_pago" , 'tipo_documento' , 'sueldo_base' , 'valores_diario__valor_diario' )


    for row in rows:
        row_num += 1
        
        for col_num in range(len(row)):
            if(col_num == 1):
               ap= row[col_num].split(' ')
               ws.write(row_num, col_num, ap[0], font_style)
            elif(col_num == 2):
                ap= row[1].split(' ')
                ws.write(row_num, col_num, ap[1], font_style)
            elif(col_num == 3):
                nom = row[col_num].split(' ')
                largo = len(nom)
                ws.write(row_num, col_num, nom[0], font_style)
            elif(col_num == 4):
                nom = row[3].split(' ')
                largo = len(nom)
                if (largo == 1):
                    ws.write(row_num, col_num,'', font_style)
                else:
                    ws.write(row_num, col_num, nom[1], font_style)
            elif(col_num == 8):
                ws.write(row_num, col_num, '0001', font_style)
            elif(col_num == 11 or col_num == 12 or col_num == 18 or col_num == 19 or col_num == 20 
            or col_num == 21 or col_num == 24  or col_num == 28  or col_num == 29  or col_num == 30  or col_num == 31  or col_num == 32
            or col_num == 34 or col_num == 36 or col_num == 37  or col_num == 38  or col_num == 41 or col_num == 42 or col_num == 43 or col_num == 44 or col_num == 45 
            or col_num == 46 or col_num == 47 or col_num == 48 or col_num == 49 or col_num == 51 or col_num == 52 or col_num == 53 or col_num == 54 or col_num == 55
            or col_num == 65 or col_num == 66 or col_num == 67  or col_num == 69 or col_num == 70 or col_num == 73 or col_num == 74 or col_num == 84
            or col_num == 87 or col_num == 88 or col_num == 89 or col_num == 93):
                ws.write(row_num, col_num, '', font_style)
            elif(col_num == 15 ):
                sexo = row[col_num]
                if(sexo == 'Masculino'):
                    sexo = 'M'
                else:
                    sexo = 'F'
                ws.write(row_num, col_num, sexo, font_style)
            elif(col_num == 16 ):
                civil = row[col_num]
                if(civil == 'Soltero(a)'):
                    civil = 'S'
                elif(civil == 'Casado(a)'):
                    civil = 'C'
                elif(civil == 'Viudo(a)'):
                    civil = 'V'
                else:
                    civil='D'
                ws.write(row_num, col_num, civil, font_style)
            elif(col_num == 17 or col_num == 56 or col_num == 57 or col_num == 58 ):
                ws.write(row_num, col_num, row[col_num].strftime("%d-%m-%Y"), font_style)
            elif(col_num == 22):
                ws.write(row_num, col_num, '0', font_style)
            elif(col_num == 35  ):
                ws.write(row_num, col_num,'P', font_style)
            elif(col_num == 40 ):
                if(row[col_num] is None):
                    ws.write(row_num, col_num,'P', font_style)
                else:
                    ws.write(row_num, col_num,'UF', font_style)
            elif(col_num == 59 ):
                ws.write(row_num, col_num,'ZZ', font_style)
            elif(col_num == 60 ):
                ws.write(row_num, col_num,'003', font_style)
            elif(col_num == 72 ):
                ws.write(row_num, col_num,'AO', font_style)
            elif(col_num == 76 ):
                ws.write(row_num, col_num,'CTPF', font_style)
            elif(col_num == 80 ):
                if(row[col_num] == 'URG'):
                    ws.write(row_num, col_num,'2', font_style)
                elif(row[col_num] == 'NOR'):
                    ws.write(row_num, col_num,'1', font_style)
                elif(row[col_num] == 'CON'):
                    ws.write(row_num, col_num,'3', font_style)
                else:
                    ws.write(row_num, col_num,'0', font_style)
            elif(col_num == 81 ):
                if (row[col_num] == True):
                    ws.write(row_num, col_num,'1', font_style)
                else:
                    ws.write(row_num, col_num,'2', font_style)
            elif(col_num == 85 ):
                if (row[col_num] != 1):
                    ws.write(row_num, col_num,'1', font_style)
                else:
                    ws.write(row_num, col_num,'', font_style)
            elif(col_num == 86 ):
                if(row[col_num] == 9):
                    ws.write(row_num, col_num,'4', font_style)
                else:
                    ws.write(row_num, col_num,'1', font_style)
            elif(col_num == 90):
                if(row[col_num] is None):
                    ws.write(row_num, col_num,'', font_style)
                else:
                    ws.write(row_num, col_num, row[col_num].strftime("%d-%m-%Y"), font_style)
            elif(col_num == 91 ):
                if(row[col_num] == 8):
                    ferido = round((row[92] / 30 ) * 1.25) / 30
                    feriadorendeado = round(ferido)
                    total = feriadorendeado + row[93]
                    ws.write(row_num, col_num, feriadorendeado, font_style)
                else:
                    ws.write(row_num, col_num, '', font_style)
            elif(col_num == 92 ):
                if(row[91] == 8):
                    ferido = round((row[92] / 30 ) * 1.25) / 30
                    feriadorendeado = round(ferido)
                    total = feriadorendeado + row[93]
                    ws.write(row_num, col_num, total, font_style)
                else:
                    ws.write(row_num, col_num, '', font_style)
        
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response



@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def exportar_excel_contrato_pendiente(request):


    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('reporte')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Solicitante','Nombres Trabajador','Rut','correo','Nacionalidad','F. Nacimiento', 'E. Civil', 'Domicilio','Comuna',  'Cargo', 'Sueldo Base', 'Sueldo Base Palabras', 'AFP',
                'Salud', 'UF pactada', 'Fecha Ingreso', 'Fecha Termino', 'Letra Causal', 'Motivo', 'Telefono', 'Turno', 'Referido', 'Centro de Costo',
                'Codigo CC', 'Area de Trabajo', 'Nivel Educacional', 'Planta','nombre banco', 'tipo cuenta', 'cuenta banco', 'Nombre Req', 'Codigo Req', 'Fecha Solicitud Req', 'Fecha Inicio Req', 'Fecha Termino Req',
 ]

    for col_num in range(len(columns)):
        
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()


    rows = Contrato.objects.filter(estado_contrato='PV', status=True).values_list('created_by__first_name','created_by__last_name','trabajador__first_name',  'trabajador__last_name',  'trabajador__rut', 'trabajador__email', 'trabajador__nacionalidad__nombre' ,
    'trabajador__fecha_nacimiento', 'trabajador__estado_civil__nombre', 'trabajador__domicilio', 'trabajador__ciudad__nombre', 'requerimiento_trabajador__area_cargo__cargo__nombre', 'sueldo_base', 'sueldo_base', 'trabajador__afp__nombre', 'trabajador__salud__nombre', 'trabajador__pacto_uf', 'fecha_inicio',
     'fecha_termino' , 'causal__nombre' , 'motivo', 'trabajador__telefono' , 'horario__nombre', 'requerimiento_trabajador__referido', 'planta__nombre' , 'requerimiento_trabajador__requerimiento__centro_costo', 'requerimiento_trabajador__requerimiento__areacargo__area__nombre', 'trabajador__nivel_estudio__nombre',
     'planta__cliente__razon_social', 'trabajador__banco__nombre', 'trabajador__tipo_cuenta__nombre', 'trabajador__cuenta', 'requerimiento_trabajador__requerimiento__nombre' , 'requerimiento_trabajador__requerimiento__codigo', 'requerimiento_trabajador__requerimiento__fecha_solicitud' ,
     'requerimiento_trabajador__requerimiento__fecha_inicio', 'requerimiento_trabajador__requerimiento__fecha_termino' )


    for row in rows:
        row_num += 1
        
        for col_num in range(len(row)):
            if(col_num == 0):
                ws.write(row_num, col_num, row[0] + ' ' + row[1] , font_style)
            if(col_num == 1):
                ws.write(row_num, col_num, row[2] + ' ' + row[3] , font_style)
            if(col_num == 2):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 3):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 4):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 5):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            if(col_num == 6):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 7):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 8):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 9):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 10):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 11):
                numero = col_num + 2
                ws.write(row_num, col_num, numero_a_letras(row[numero]), font_style)
            if(col_num == 12):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 13):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 14):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 15):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            if(col_num == 16):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            if(col_num == 17):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 18):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 19):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 20):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 21):
                numero = col_num + 2
                if (row[numero] ==  True):
                    referido = 'SI'
                else:
                    referido = 'NO'
                ws.write(row_num, col_num, referido, font_style)
            if(col_num == 22):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 23):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 24):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 25):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 26):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 27):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 28):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 29):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 30):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 31):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 32):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            if(col_num == 33):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            if(col_num == 34):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            # else:
            #     ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response



@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def exportar_excel_contrato_normal(request):

    planta = request.POST.get('planta')
    mes = request.POST.get('mes')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('reporte')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Solicitante','Nombres Trabajador','Rut','correo','Nacionalidad','F. Nacimiento', 'E. Civil', 'Domicilio','Comuna',  'Cargo', 'Sueldo Base', 'Sueldo Base Palabras', 'AFP',
                'Salud', 'UF pactada', 'Fecha Ingreso', 'Fecha Termino', 'Letra Causal', 'Motivo', 'Telefono', 'Turno', 'Referido', 'Centro de Costo',
                'Codigo CC', 'Area de Trabajo', 'Nivel Educacional', 'Planta','nombre banco', 'tipo cuenta', 'cuenta banco', 'Nombre Req', 'Codigo Req', 'Fecha Solicitud Req', 'Fecha Inicio Req', 'Fecha Termino Req',
 ]

    for col_num in range(len(columns)):
        
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()


    rows = Contrato.objects.filter(estado_contrato='AP', planta_id=planta, fecha_inicio__month=mes, status=True).values_list('created_by__first_name','created_by__last_name','trabajador__first_name',  'trabajador__last_name',  'trabajador__rut', 'trabajador__email', 'trabajador__nacionalidad__nombre' ,
    'trabajador__fecha_nacimiento', 'trabajador__estado_civil__nombre', 'trabajador__domicilio', 'trabajador__ciudad__nombre', 'requerimiento_trabajador__area_cargo__cargo__nombre', 'sueldo_base', 'sueldo_base', 'trabajador__afp__nombre', 'trabajador__salud__nombre', 'trabajador__pacto_uf', 'fecha_inicio',
     'fecha_termino' , 'causal__nombre' , 'motivo', 'trabajador__telefono' , 'horario__nombre', 'requerimiento_trabajador__referido', 'planta__nombre' , 'requerimiento_trabajador__requerimiento__centro_costo', 'requerimiento_trabajador__requerimiento__areacargo__area__nombre', 'trabajador__nivel_estudio__nombre',
     'planta__cliente__razon_social', 'trabajador__banco__nombre', 'trabajador__tipo_cuenta__nombre', 'trabajador__cuenta', 'requerimiento_trabajador__requerimiento__nombre' , 'requerimiento_trabajador__requerimiento__codigo', 'requerimiento_trabajador__requerimiento__fecha_solicitud' ,
     'requerimiento_trabajador__requerimiento__fecha_inicio', 'requerimiento_trabajador__requerimiento__fecha_termino' )


    for row in rows:
        row_num += 1
        
        for col_num in range(len(row)):
            if(col_num == 0):
                ws.write(row_num, col_num, row[0] + ' ' + row[1] , font_style)
            if(col_num == 1):
                ws.write(row_num, col_num, row[2] + ' ' + row[3] , font_style)
            if(col_num == 2):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 3):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 4):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 5):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            if(col_num == 6):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 7):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 8):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 9):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 10):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 11):
                numero = col_num + 2
                ws.write(row_num, col_num, numero_a_letras(row[numero]), font_style)
            if(col_num == 12):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 13):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 14):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 15):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            if(col_num == 16):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            if(col_num == 17):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 18):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 19):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 20):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 21):
                numero = col_num + 2
                if (row[numero] ==  True):
                    referido = 'SI'
                else:
                    referido = 'NO'
                ws.write(row_num, col_num, referido, font_style)
            if(col_num == 22):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 23):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 24):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 25):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 26):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 27):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 28):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 29):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 30):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 31):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero], font_style)
            if(col_num == 32):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            if(col_num == 33):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            if(col_num == 34):
                numero = col_num + 2
                ws.write(row_num, col_num, row[numero].strftime("%d %B %Y"), font_style)
            # else:
            #     ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def create(request):
    
    requerimientotrabajador = request.POST['requerimiento_trabajador_id']
    trabajador = get_object_or_404(Trabajador, pk=request.POST['trabajador_id'])

    # Trae el id del Requerimiento
    requer = RequerimientoTrabajador.objects.values_list('requerimiento', flat=True).get(pk=requerimientotrabajador, status=True)
    # Trae el id de la planta del Requerimiento
    plant_template = Requerimiento.objects.values_list('planta', flat=True).get(pk=requer, status=True)
    # Busca si la planta tiene plantilla 
    if not Plantilla.objects.filter(plantas=plant_template, tipo_id=10).exists():
        # Trae las plantillas (formatos) que tiene la planta. tipo_id=10=Doc. Adicionales
        formato = Plantilla.objects.values('archivo', 'abreviatura', 'tipo_id').filter(plantas=plant_template, tipo_id=10)
        messages.error(request, 'La Planta no posee Plantilla asociada. Por favor gestionar con el Dpto. de Contratos')
        return redirect('contratos:create_contrato', requerimientotrabajador)
    # exit()
    if (request.POST['tipo'] == 'diario'):
        formato = Plantilla.objects.values('archivo', 'abreviatura', 'tipo_id').filter( Q(tipo_id=10) |  Q(tipo_id=13), plantas=plant_template)
    else: 
        formato = Plantilla.objects.values('archivo', 'abreviatura', 'tipo_id').filter(plantas=plant_template, tipo_id=10)


    contrato = Contrato()
    contrato.causal_id = request.POST['causal']
    contrato.motivo = request.POST['motivo']
    contrato.regimen = request.POST['regimen']
    if request.POST['tipo'] == 'mensual':
        contrato.fecha_inicio = request.POST['fecha_inicio']
        contrato.fecha_termino = request.POST['fecha_termino']
        contrato.fecha_termino_ultimo_anexo = request.POST['fecha_termino']
        contrato.tipo_documento_id = request.POST['tipo_documento']
        contrato.sueldo_base = request.POST['sueldo_base']
    else:
        sueldomensual = ValoresDiarioAfp.objects.values_list('valor', flat=True).get(valor_diario_id =request.POST['valores_diario'], status=True, afp_id = trabajador.afp.id ) 
        contrato.sueldo_base = sueldomensual
        try:
            contrato.fecha_inicio = request.POST['fecha_inicio']
            contrato.fecha_termino = request.POST['fecha_inicio']
            contrato.fecha_termino_ultimo_anexo = request.POST['fecha_inicio']
            fecha_inicio = request.POST['fecha_inicio']
        except:
            contrato.fecha_inicio = request.POST['fecha_inicio_diario']
            contrato.fecha_termino = request.POST['fecha_inicio_diario']
            contrato.fecha_termino_ultimo_anexo = request.POST['fecha_inicio_diario']
            fecha_inicio = request.POST['fecha_inicio_diario']

        contrato.tipo_documento_id = 8
        contrato.valores_diario_id = request.POST['valores_diario']
        test_date = date.fromisoformat(fecha_inicio)
        weekday_idx = 3
        days_delta = weekday_idx - test_date.weekday()
        if days_delta <= 7:
            days_delta += 7
        res = test_date + timedelta(days_delta)
        contrato.fecha_pago = res
    contrato.horario_id = request.POST['horario']
    contrato.gratificacion_id = request.POST['gratificacion']
    contrato.planta_id = request.POST['planta']
    contrato.trabajador_id = request.POST['trabajador_id']
    contrato.requerimiento_trabajador_id = request.POST['requerimiento_trabajador_id'] 
    contrato.status = True
    contrato.save()
    largobonos = int(request.POST['largobonos']) + 1
    i = []
    for a in range(1,largobonos):
        i = request.POST.getlist(str(a))
        if (i[0] != '0'):
            bonos = ContratosBono()
            bonos.valor = i[0]
            bonos.bono_id = i[1]
            bonos.contrato_id = contrato.id
            bonos.save()

    # Doc. Adicionales
    # Trae el id de la planta del Requerimiento
    plant_template = Contrato.objects.values_list('planta', flat=True).get(pk=contrato.id, status=True)
    # Trae las plantillas (formatos) que tiene la planta. tipo_id=10=Doc. Adicionales
    
    for formt in formato:
        # import yaml
        now = datetime.now()
        fecha_nacimiento = Contrato.objects.values_list('trabajador__fecha_nacimiento', flat=True).get(pk=contrato.id, status=True)
        doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT + '/' + formt['archivo']))
        # Variables de Doc. Adicionales
        context = { 'fecha_ingreso_trabajador_palabras': fecha_a_letras(contrato.fecha_inicio),
                    'nombres_trabajador': contrato.trabajador.first_name,
                    'apellidos_trabajador': contrato.trabajador.last_name,
                    'rut_trabajador': contrato.trabajador.rut,
                    'comuna_trabajador': contrato.trabajador.ciudad.nombre,
                    'domicilio_trabajador': contrato.trabajador.domicilio,
                    'nacionalidad': contrato.trabajador.nacionalidad.nombre,
                    'fono': contrato.trabajador.telefono,
                    'dd': format(fecha_nacimiento.day),
                    'mm': format(fecha_nacimiento.month),
                    'aaaa': format(fecha_nacimiento.year),
                    'fecha_nacimiento': fecha_a_letras(contrato.trabajador.fecha_nacimiento),
                    'sexo_trabajador': contrato.trabajador.sexo.nombre,
                    'estado_civil': contrato.trabajador.estado_civil.nombre,
                    'prevision_trabajador': contrato.trabajador.afp.nombre,
                    'salud_trabajador': contrato.trabajador.salud.nombre,
                    'adicional_cumplimiento_horario_undecimo': 'SIN INFORMACIÓN',
                    'parrafo_decimo_tercero': 'SIN INFORMACIÓN',
                    'fecha_ingreso_trabajador': fecha_a_letras(contrato.fecha_inicio),
                    'fecha_termino_trabajador': fecha_a_letras(contrato.fecha_termino),
                    'fecha_vigencia_contrato': 'SIN INFORMACIÓN',
        }
        rut_trabajador = contrato.trabajador.rut
        doc.render(context)

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

        # Contratos Parametros General, ruta_documentos donde guardara el documento
        ruta_documentos = ContratosParametrosGen.objects.values_list('ruta_documentos', flat=True).get(pk=1, status=True)
        path = os.path.join(ruta_documentos)
        # Si carpeta no existe, crea carpeta de contratos.
        carpeta = 'contratos'
        try:
            os.mkdir(path + carpeta)
            path = os.path.join(settings.MEDIA_ROOT + '/contratos/')
            doc.save(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id)  + '.docx')
            win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
            # convert("Contrato#1.docx")

            convert(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".docx", path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf")
            url = str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf"
            contrato.archivo = 'contratos/' + url
            doc_contrato = DocumentosContrato(contrato=contrato, archivo=url)
            doc_contrato.tipo_documento_id = formt['tipo_id']
            doc_contrato.save()
            # Elimino el documento word.
            os.remove(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + '.docx')
            messages.success(request, 'Contrato Creado Exitosamente')
        except:
            path = os.path.join(settings.MEDIA_ROOT + '/contratos/')
            doc.save(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id)  + '.docx')
            win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
            # convert("Contrato#1.docx")

            convert(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".docx", path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf")
            url = str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf"
            contrato.archivo = 'contratos/' + url
            # tipo_documento = []
            # if formt['nombre'] == 'Carta de Término':
            #     tipo_documento = 6
            # if formt['nombre'] == 'Seguro de Vida':
            #     tipo_documento = 5
            doc_contrato = DocumentosContrato(contrato=contrato, archivo=url)
            doc_contrato.tipo_documento_id = formt['tipo_id']
            doc_contrato.save()
            # Elimino el documento word.
            os.remove(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + '.docx')
            messages.success(request, 'Contrato Creado Exitosamente')
    return redirect('contratos:create_contrato', requerimientotrabajador)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def aprobacion_masiva(request, aprobacion):
  
    lista_aprobacion = aprobacion.split(',')
    for i in lista_aprobacion:
        revision = Revision.objects.get(contrato_id=i)
        revision.estado = 'AP'
        revision.save()
        contrato = Contrato.objects.get(pk=i)
        contrato.fecha_aprobacion  = datetime.now()
        contrato.estado_contrato = 'AP'
        finiquito(contrato.id)
        contrato.save()
        fecha_ingreso_trabajador_palabras = fecha_a_letras(contrato.fecha_inicio)
        send_mail(
                'Nueva Solicitud en SGO3 | Contrato',
                'Estimado(a) la solicitud de contrato para el trabajador ' + str(contrato.trabajador.first_name) +' '+str(contrato.trabajador.last_name)+' con fecha de ingreso: ' 
                + str(fecha_ingreso_trabajador_palabras) + ' para la planta: '+ str(contrato.planta.nombre)+' ha sido APROBADA',
                contrato.created_by.email,
                ['contratos@empresasintegra.cl', 'soporte@empresasintegra.cl', contrato.created_by.email],
                fail_silently=False,
        )
        messages.success(request, 'Contratos aprobados Exitosamente')
        data = True
    return JsonResponse(data, safe=False)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def update_contrato(request, contrato_id, template_name='contratos/contrato_update.html'):
            data = dict()
            contrato = get_object_or_404(Contrato, pk=contrato_id)
            trabajador = get_object_or_404(Trabajador, pk=contrato.trabajador_id)
            try:
                revision = Revision.objects.get(contrato_id=contrato_id)
            except:
                 revision = ''
  
   
            requer_trabajador = get_object_or_404(RequerimientoTrabajador, pk=contrato.requerimiento_trabajador_id)
            if request.method == 'POST':
                
                contrato.motivo = request.POST['motivo']
                
                contrato.horario_id = request.POST['horario']
                contrato.status = True
                contrato.regimen = request.POST['regimen']
                if request.POST['tipo2'] == 'mensual':
                    contrato.fecha_inicio = request.POST['fecha_inicio']
                    contrato.fecha_termino = request.POST['fecha_termino']
                    contrato.fecha_termino_ultimo_anexo = request.POST['fecha_termino']
                    contrato.tipo_documento_id = request.POST['tipo_documento']
                    contrato.sueldo_base = request.POST['sueldo_base']
                else:
                    sueldomensual = ValoresDiarioAfp.objects.values_list('valor', flat=True).get(valor_diario_id =request.POST['valores_diario'], status=True, afp_id = trabajador.afp.id )
                    contrato.sueldo_base = sueldomensual
                    try:
                        contrato.fecha_inicio = request.POST['fecha_inicio']
                        contrato.fecha_termino = request.POST['fecha_inicio']
                        contrato.fecha_termino_ultimo_anexo = request.POST['fecha_inicio']
                        fecha_inicio = request.POST['fecha_inicio']
                    except:
                        contrato.fecha_inicio = request.POST['fecha_inicio_diario']
                        contrato.fecha_termino = request.POST['fecha_inicio_diario']
                        contrato.fecha_termino_ultimo_anexo = request.POST['fecha_inicio_diario']
                        fecha_inicio = request.POST['fecha_inicio_diario']
                    contrato.tipo_documento_id = 8
                    contrato.valores_diario_id = request.POST['valores_diario']                    
                    test_date = date.fromisoformat(fecha_inicio)
                    weekday_idx = 3
                    days_delta = weekday_idx - test_date.weekday()
                    if days_delta <= 7:
                        days_delta += 7
                        res = test_date + timedelta(days_delta)
                        contrato.fecha_pago = res
                contrato.save()
                bonos = []
                bonosguardados = ContratosBono.objects.values_list('id', flat=True).filter(contrato_id=contrato_id) 
                for i in bonosguardados:
                    bonos.append(i) 
                for a in bonos:
                    bonoseliminar = ContratosBono.objects.get(id = a)
                    bonoseliminar.delete()
                largobonos = int(request.POST['largobonos']) + 1
                i = []
                for a in range(1,largobonos):
                    i = request.POST.getlist(str(a))
                    if (i[0] != '0' ):
                        bonos = ContratosBono()
                        bonos.valor = i[0]
                        bonos.bono_id = i[1]
                        bonos.contrato_id = contrato.id
                        bonos.save()
                return redirect('contratos:create_contrato',contrato.requerimiento_trabajador_id)
            else:
                form = ContratoEditarForm(instance=contrato,horario=requer_trabajador.requerimiento.cliente.horario.all())
                tipo_contrato = Contrato.objects.values_list('tipo_documento', flat=True).get(pk=contrato_id, status=True)
                req = contrato.requerimiento_trabajador_id 
                bonos = RequerimientoTrabajador.objects.raw("SELECT b.id, b.nombre, cb.valor FROM public.requerimientos_requerimientotrabajador as rt LEFT JOIN public.requerimientos_requerimiento as r on r.id = rt.requerimiento_id LEFT JOIN public.clientes_planta as p on p.id = r.planta_id LEFT JOIN public.clientes_planta_bono as pb on pb.planta_id = p.id LEFT JOIN public.utils_bono as b on b.id = pb.bono_id LEFT JOIN public.contratos_contrato as c on c.requerimiento_trabajador_id = rt.id LEFT JOIN public.contratos_contratosbono as cb on cb.bono_id = pb.bono_id WHERE rt.id = %s ORDER BY cb.valor" , [req])
                largobonos = len(bonos)
                context={
                    'form4': form,
                    'contrato':contrato,
                    'tipo_contrato':tipo_contrato,
                    'contrato_id': contrato_id,
                    'largobonos' : largobonos,
                    'revision' : revision,
                    'bonos' : bonos
                }
                data['html_form'] = render_to_string(
                    template_name,
                    context,
                    request=request,
                )
                return JsonResponse(data)


@login_required
def delete(request, object_id, template_name='contratos/contrato_delete.html'):
    data = dict()
    object = get_object_or_404(Contrato, pk=object_id)
    pk = object.requerimiento_trabajador.id
    doc_adicionales = DocumentosContrato.objects.values_list('archivo', flat=True).filter(contrato=object)

    if request.method == 'POST':
        try:
            # Contratos Parametros General, ruta_documentos donde guardara el/los documento(s)
            ruta_documentos = ContratosParametrosGen.objects.values_list('ruta_documentos', flat=True).get(pk=1, status=True)
            path = os.path.join(ruta_documentos)
            # Elimina los documento adicionales del contrato.
            for e in doc_adicionales:
                os.remove(path + "contratos/" + str(e))

            object.delete()
            messages.success(request, 'Contrato eliminado Exitosamente')
        except ProtectedError:
            messages.error(request, 'El contrato no se pudo eliminar.')
            return redirect('contratos:create_contrato', pk)

        return redirect('contratos:create_contrato', pk)

    context = {'object': object}
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request
    )
    return JsonResponse(data)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def solicitudes_pendientes(request, contrato_id, template_name='contratos/contrato_pdf.html'):
    data = dict()
    contrato = get_object_or_404(Contrato, pk=contrato_id)

    context = {'contrato': contrato, }
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def solicitudes_pendientes_baja(request, contrato_id, template_name='contratos/modal_baja_anexo.html'):
    data = dict()
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    baja = get_object_or_404(Baja, contrato_id=contrato_id)


    context = {
        'contrato': contrato,
        'baja': baja
         }
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def baja_contrato(request, contrato_id, template_name='contratos/baja_contrato.html'): 
    data = dict()
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    if request.method == 'POST':
        contrato.estado_contrato = 'PB'
        contrato.fecha_solicitud_baja = datetime.now()
        contrato.save()
        baja = Baja()
        baja.contrato_id = contrato_id
        baja.motivo_id = request.POST['motivo']
        baja.save()
        

        fecha_ingreso_trabajador_palabras = fecha_a_letras(contrato.fecha_inicio)
        send_mail(
            'Nueva Solicitud en SGO3 | Contrato Baja',
            'Estimado(a) se ha solicitado una baja de contrato para el trabajador: ' + str(contrato.trabajador.first_name) +' '+str(contrato.trabajador.last_name)+' con fecha de ingreso: ' 
            + str(fecha_ingreso_trabajador_palabras) + ' para la planta: '+ str(contrato.planta.nombre) +' por el motivo ' + baja.motivo.nombre,
            contrato.created_by.email,
            ['contratos@empresasintegra.cl', 'soporte@empresasintegra.cl', contrato.created_by.email],
            fail_silently=False,
                )
        messages.success(request, 'Contrato enviado a proceso de baja Exitosamente')
        return redirect('contratos:create_contrato',contrato.requerimiento_trabajador_id)

    else:
    
        context = {
            'form10': MotivoBajaForm,
            'contrato': contrato,
            'contrato_id': contrato_id, 
            }
        data['html_form'] = render_to_string(
            template_name,
            context,
            request=request,
        )
        return JsonResponse(data)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def enviar_revision_contrato(request, contrato_id):
            contrato = get_object_or_404(Contrato, pk=contrato_id)
            # Trae el id de la planta del Requerimiento
            plant_template = Contrato.objects.values_list('planta', flat=True).get(pk=contrato_id, status=True)
            # Busca si la planta tiene plantilla 
            if not Plantilla.objects.filter(plantas=plant_template,  tipo_id=contrato.tipo_documento).exists():
                messages.error(request, 'La Planta no posee Plantilla asociada. Por favor gestionar con el Dpto. de Contratos')
                return redirect('contratos:create_contrato', contrato.requerimiento_trabajador_id)

            else:
                contrato.estado_contrato = 'PV'
                contrato.fecha_solicitud = datetime.now()
                
                try:
                    revision = Revision.objects.get(contrato_id=contrato_id)
                    revision.estado = 'PD'
                    revision.save()
                except:  
                    revision = Revision()
                    revision.contrato_id = contrato.id
                    revision.save()
                # Trae la plantilla que tiene la planta
                if(contrato.horario.id == 1):
                    formato = Plantilla.objects.values('archivo', 'abreviatura', 'tipo_id').filter(plantas=plant_template, tipo_id=contrato.tipo_documento)
                else:
                    formato = Plantilla.objects.values('archivo', 'abreviatura', 'tipo_id').filter(Q(tipo_id=contrato.tipo_documento) |  Q(tipo_id=14), plantas=plant_template)
                
                if(contrato.valores_diario != None):
                    valor_mensual=Contrato.objects.values_list('valores_diario__valor_diario', flat=True).get(pk=contrato_id, status=True)
                    valor_mensual_palabras = numero_a_letras(Contrato.objects.values_list('valores_diario__valor_diario', flat=True).get(pk=contrato_id, status=True))+' pesos'
                else:
                    valor_mensual=Contrato.objects.values_list('sueldo_base', flat=True).get(pk=contrato_id, status=True)
                    valor_mensual_palabras = numero_a_letras(Contrato.objects.values_list('sueldo_base', flat=True).get(pk=contrato_id, status=True))+' pesos'
                    
                for formt in formato:
                    now = datetime.now()
                    doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT + '/' + formt['archivo']))
                    # Variables de Contrato
                    print('fehca larga', Contrato.objects.values_list('fecha_termino', flat=True).get(pk=contrato.id, status=True))
                    print('fehca larga letra', fecha_a_letras(Contrato.objects.values_list('fecha_termino', flat=True).get(pk=contrato.id, status=True)))
                    print('fehca corta', contrato.fecha_termino)
                    context = { 'codigo_req': contrato.requerimiento_trabajador.requerimiento.codigo,
                                'rut_planta': contrato.planta.rut,
                                'nombre_planta': contrato.planta.nombre,
                                'region_planta': contrato.planta.region2.nombre,
                                'comuna_planta': contrato.planta.ciudad2.nombre,
                                'direccion_planta': contrato.planta.direccion,
                                'descripcion_jornada': contrato.horario.descripcion,
                                'gratificacion': contrato.gratificacion.descripcion,
                                'fecha_ingreso_trabajador_palabras': fecha_a_letras(contrato.fecha_inicio),
                                'rut_trabajador': contrato.trabajador.rut,
                                'nombres_trabajador': contrato.trabajador.first_name,
                                'apellidos_trabajador': contrato.trabajador.last_name,
                                'nacionalidad': contrato.trabajador.nacionalidad.nombre,
                                'fecha_nacimiento': fecha_a_letras(contrato.trabajador.fecha_nacimiento),
                                'estado_civil': contrato.trabajador.estado_civil.nombre,
                                'domicilio_trabajador': contrato.trabajador.domicilio,
                                'comuna_trabajador': contrato.trabajador.ciudad.nombre,
                                'nombre_banco': contrato.trabajador.banco.nombre,
                                'cuenta': contrato.trabajador.cuenta,
                                'correo': contrato.trabajador.email,
                                'prevision_trabajador': contrato.trabajador.afp.nombre,
                                'salud_trabajador': contrato.trabajador.salud.nombre,
                                'centro_costo': contrato.requerimiento_trabajador.requerimiento.centro_costo,
                                'descripcion_causal': contrato.causal.descripcion,
                                'motivo_req': contrato.motivo,
                                'cargo_postulante': contrato.requerimiento_trabajador.area_cargo.cargo.nombre,
                                'sueldo_base_numeros': valor_mensual,
                                'sueldo_base_palabras':  valor_mensual_palabras,
                                'detalle_bonos': 'SIN INFORMACIÓN',
                                'adicional_cumplimiento_horario_undecimo': 'SIN INFORMACIÓN',
                                'parrafo_decimo_tercero': 'SIN INFORMACIÓN',
                                'fecha_ingreso_trabajador': fecha_a_letras(contrato.fecha_inicio),
                                'fecha_ingreso': contrato.fecha_inicio,
                                'fecha_termino_trabajador': fecha_a_letras(contrato.fecha_termino),
                                'fecha_termino': contrato.fecha_termino,
                                }
                    rut_trabajador =  contrato.trabajador.rut
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

                    # Contratos Parametros General, ruta_documentos donde guardara el documento
                    ruta_documentos = ContratosParametrosGen.objects.values_list('ruta_documentos', flat=True).get(pk=1, status=True)
                    path = os.path.join(ruta_documentos)
                    # Si carpeta no existe, crea carpeta de contratos.
                    carpeta = 'contratos'

                    try:
                        os.mkdir(path + carpeta)
                        path = os.path.join(settings.MEDIA_ROOT + '/contratos/')
                        doc.save(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato_id)  + '.docx')
                        win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
                        # convert("Contrato#1.docx")

                        convert(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato_id) + ".docx", path +  str(rut_trabajador) + "_" + formt['abreviatura'] + "_" +  str(contrato_id) + ".pdf")
                        if(formt['tipo_id'] == contrato.tipo_documento.id):
                            url = str(rut_trabajador) + "_new_" + formt['abreviatura'] + "_" + str(contrato_id) + ".pdf"
                            contrato.archivo = 'contratos/' + url
                            contrato.save()
                        else:
                            url = str(rut_trabajador) + "_new_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf"
                            contrato.archivo = 'contratos/' + url
                            doc_contrato = DocumentosContrato(contrato=contrato, archivo=url)
                            doc_contrato.tipo_documento_id = formt['tipo_id']
                            doc_contrato.save()
                         
                           

                        nombre_trabajador = Contrato.objects.values_list('trabajador__first_name', flat=True).get(pk=contrato_id, status=True)
                        apellido = Contrato.objects.values_list('trabajador__last_name', flat=True).get(pk=contrato_id, status=True)
                        fecha_ingreso_trabajador_palabras = fecha_a_letras(Contrato.objects.values_list('fecha_inicio', flat=True).get(pk=contrato_id, status=True))
                        nombre_planta = Contrato.objects.values_list('planta__nombre', flat=True).get(pk=contrato_id, status=True)
                        send_mail(
                            'Nueva Solicitud en SGO3 | Contrato Revisión',
                            'Estimado(a) se a realizado un solicitud de revisión de contrato para el trabajador ' + str(nombre_trabajador) +' '+str(apellido)+' con fecha de ingreso: ' 
                            + str(fecha_ingreso_trabajador_palabras) + ' para la planta: '+ nombre_planta,
                            contrato.created_by.email,
                            ['contratos@empresasintegra.cl', 'soporte@empresasintegra.cl', contrato.created_by.email],
                            fail_silently=False,
                        )
                        
                        # Elimino el documento word.
                        os.remove(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato_id) + '.docx')
                        messages.success(request, 'Contrato enviado a revisión Exitosamente')
                    except:
                        path = os.path.join(settings.MEDIA_ROOT + '/contratos/')
                        doc.save(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato_id)  + '.docx')
                        win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
                        # convert("Contrato#1.docx")

                        convert(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato_id) + ".docx", path +  str(rut_trabajador) + "_" + formt['abreviatura'] + "_" +  str(contrato_id) + ".pdf")
                        if(formt['tipo_id'] == contrato.tipo_documento.id):
                            url = str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato_id) + ".pdf"
                            contrato.archivo = 'contratos/' + url
                            contrato.save()
    
                        else:
                            url = str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf"
                            contrato.archivo = 'contratos/' + url
                            doc_contrato = DocumentosContrato(contrato=contrato, archivo=url)
                            doc_contrato.tipo_documento_id = formt['tipo_id']
                            doc_contrato.save()


                        nombre_trabajador = Contrato.objects.values_list('trabajador__first_name', flat=True).get(pk=contrato_id, status=True)
                        apellido = Contrato.objects.values_list('trabajador__last_name', flat=True).get(pk=contrato_id, status=True)
                        fecha_ingreso_trabajador_palabras = fecha_a_letras(Contrato.objects.values_list('fecha_inicio', flat=True).get(pk=contrato_id, status=True))
                        nombre_planta = Contrato.objects.values_list('planta__nombre', flat=True).get(pk=contrato_id, status=True)
                        send_mail(
                            'Nueva Solicitud en SGO3 | Contrato Revisión',
                            'Estimado(a) se a realizado un solicitud de revisión de contrato para el trabajador ' + str(nombre_trabajador) +' '+str(apellido)+' con fecha de ingreso: ' 
                            + str(fecha_ingreso_trabajador_palabras) + ' para la planta: '+ nombre_planta,
                            contrato.created_by.email,
                            ['contratos@empresasintegra.cl', 'soporte@empresasintegra.cl', contrato.created_by.email],
                            fail_silently=False,
                        )
                        
                        # Elimino el documento word.
                        os.remove(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato_id) + '.docx')
                        messages.success(request, 'Contrato enviado a revisión Exitosamente')
                
                return redirect('contratos:create_contrato', contrato.requerimiento_trabajador_id)


@login_required
@permission_required('contratos.add_finrequerimiento', raise_exception=True)
def carta_termino(request):

    requerimientotrabajador = request.POST['requerimiento_trabajador_id']
    
    # Trae el id del Requerimiento
    requer = RequerimientoTrabajador.objects.values_list('requerimiento', flat=True).get(pk=requerimientotrabajador, status=True)
    # Trae el id de la planta del Requerimiento
    plant_template = Requerimiento.objects.values_list('planta', flat=True).get(pk=requer, status=True)
    # Busca si la planta tiene plantilla 
    if not Plantilla.objects.filter(plantas=plant_template, tipo_id=9).exists():
        # Trae las plantillas (formatos) que tiene la planta. tipo_id=9=Carta Término
        formato = Plantilla.objects.values('archivo', 'abreviatura', 'tipo_id').filter(plantas=plant_template, tipo_id=9)
        messages.error(request, 'La Planta no posee Plantilla asociada. Por favor gestionar con el Dpto. de Contratos')
        return redirect('contratos:create_contrato', requerimientotrabajador)
    else:
        ct = FinRequerimiento()
        ct.tipo = request.POST['tipo']
        ct.archivo = 'Creando'
        ct.requerimiento_trabajador_id = request.POST['requerimiento_trabajador_id']
        ct.fecha_termino = request.POST['fecha_termino']
        ct.save()
        # Se actualiza el campo fin_requerimiento_id de Contrato
        contrato = Contrato.objects.get(pk=request.POST['contrato_id'])
        contrato.fin_requerimiento_id = ct.id
        contrato.save()
        # Se actualiza el campo fin_requerimiento_id de Anexo
        anexo = Anexo.objects.filter(contrato=contrato.id).update(fin_requerimiento_id = ct.id)

        formato = Plantilla.objects.values('archivo', 'abreviatura', 'tipo_id').filter(plantas=plant_template, tipo_id=9)
        for formt in formato:
            doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT + '/' + formt['archivo']))
            # Variables de Carta Término
            context = { 'fecha_vigencia_contrato': 'SIN INFORMACIÓN',
                        'fecha_ingreso_trabajador': fecha_a_letras(Contrato.objects.values_list('fecha_inicio', flat=True).get(pk=contrato.id, status=True)),
                        'nombres_trabajador': contrato.trabajador.first_name,
                        'apellidos_trabajador': contrato.trabajador.last_name,
                        'rut_trabajador': contrato.trabajador.rut,
                        # 'fecha_pago': Contrato.objects.values_list('fecha_pago', flat=True).get(pk=contrato.id, status=True),
                        'fecha_termino_trabajador': fecha_a_letras(Contrato.objects.values_list('fecha_termino', flat=True).get(pk=contrato.id, status=True)),
                                }
            rut_trabajador =  contrato.trabajador.rut
            doc.render(context)

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

            # Contratos Parametros General, ruta_documentos donde guardara el documento
            ruta_documentos = ContratosParametrosGen.objects.values_list('ruta_documentos', flat=True).get(pk=1, status=True)
            path = os.path.join(ruta_documentos)
            # Si carpeta no existe, crea carpeta de contratos.
            carpeta = 'contratos'
            try:
                os.mkdir(path + carpeta)
                path = os.path.join(settings.MEDIA_ROOT + '/contratos/')
                doc.save(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id)  + '.docx')
                win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
                # convert("Contrato#1.docx")

                convert(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".docx", path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf")
                url = str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf"
                ct = FinRequerimiento.objects.get(pk=ct.id)
                ct.archivo = 'contratos/' + url
                ct.save()
                # Elimino el documento word.
                os.remove(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + '.docx')
                messages.success(request, 'Carta de Término Creada Exitosamente')
            except:
                path = os.path.join(settings.MEDIA_ROOT + '/contratos/')
                doc.save(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id)  + '.docx')
                win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())

                convert(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".docx", path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf")
                url = str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf"
                ct = FinRequerimiento.objects.get(pk=ct.id)
                ct.archivo = 'contratos/' + url
                ct.save()
                # Elimino el documento word.
                os.remove(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + '.docx')
                messages.success(request, 'Carta de Término Creada Exitosamente')
    return redirect('contratos:create_contrato', requerimientotrabajador)


class ContratoCompletaListView(ListView):
    model = Contrato
    form_class = CompletasForm
    template_name = 'contratos/consulta_completas.html'
    
    
    def get_queryset(self):
        return Contrato.objects.filter(estado_contrato='AP', fecha_inicio__month=str(now.month), status=True)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['form'] = CompletasForm(instance=Contrato)
        context ['data'] = Contrato.objects.filter(estado_contrato='AP', fecha_inicio__month=str(now.month), status=True)
        return context

def buscar_contrato(request):
    if request.method == 'POST':
        planta = request.POST.get('planta')
        mes = request.POST.get('mes')
        if mes:
            data = Contrato.objects.filter(estado_contrato='AP', planta_id=planta, fecha_inicio__month=mes, status=True)
            context = {'data': data}
            context ['form'] = CompletasForm(instance=Contrato)
            return render(request, 'contratos/consulta_completas.html', context)
        else:
            data = Contrato.objects.filter(estado_contrato='AP', planta_id=planta, status=True)
            context = {'data': data}
            context ['form'] = CompletasForm(instance=Contrato)
            return render(request, 'contratos/consulta_completas.html', context)

def contrato_baja_completa(request, contrato_id, template_name='contratos/baja_contrato_completa.html'):
    data = dict()
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    if request.method == 'POST':
        contrato.estado_contrato = 'PB'
        contrato.fecha_solicitud_baja = datetime.now()
        contrato.save()
        baja = Baja()
        baja.contrato_id = contrato_id
        baja.motivo_id = request.POST['motivo']
        baja.save()
        return redirect('contratos:list-completa')
    else:
        context = {
            'form10': MotivoBajaForm,
            'contrato': contrato,
            'contrato_id': contrato_id, 
            }

    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


class ContratoBajaListView(ListView):
    model = Contrato
    form_class = CompletasForm
    template_name = 'contratos/consulta_bajas.html'
    
    
    def get_queryset(self):
        return Contrato.objects.filter(estado_contrato='BJ', fecha_inicio__month=str(now.month), status=True)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['form'] = CompletasForm(instance=Contrato)
        context ['data'] = Contrato.objects.filter(estado_contrato='BJ', fecha_inicio__month=str(now.month), status=True)
        return context

def buscar_baja_contrato(request):
    if request.method == 'POST':
        planta = request.POST.get('planta')
        mes = request.POST.get('mes')
        if mes:
            data = Contrato.objects.filter(estado_contrato='BJ', planta_id=planta, fecha_inicio__month=mes, status=True)
            context = {'data': data}
            context ['form'] = CompletasForm(instance=Contrato)
            return render(request, 'contratos/consulta_bajas.html', context)
        else:
            data = Contrato.objects.filter(estado_contrato='BJ', planta_id=planta, status=True)
            context = {'data': data}
            context ['form'] = CompletasForm(instance=Contrato)
            return render(request, 'contratos/consulta_bajas.html', context)


class ContratoIdView(TemplateView):
    template_name = 'contratos/create_contrato.html'

    def get_context_data(self, requerimiento_trabajador_id, **kwargs):
        anex = 'NO'
        finiquito = 'NO'
        fin_contrato = 'NO'
        # ultimo_anexo_contrato = 'NO'
        requer_trabajador = get_object_or_404(RequerimientoTrabajador, pk=requerimiento_trabajador_id, status= True)
        try:
            contrato = Contrato.objects.get(requerimiento_trabajador_id=requerimiento_trabajador_id)
            ahora = datetime.now().strftime("%Y-%m-%d")
            dias = contrato.fecha_termino_ultimo_anexo - ahora
        except:
            contrato = ''

        trabaj = RequerimientoTrabajador.objects.filter(id=requerimiento_trabajador_id).values(
                'trabajador', 'trabajador__first_name', 'trabajador__last_name', 'trabajador__rut','trabajador__estado_civil__nombre', 'trabajador__fecha_nacimiento',
                'trabajador__domicilio', 'trabajador__ciudad', 'trabajador__afp', 'trabajador__salud', 'trabajador__nivel_estudio', 'trabajador__telefono', 'trabajador__nacionalidad',
                'requerimiento__nombre',  'referido','requerimiento__areacargo', 'requerimiento__centro_costo', 'requerimiento__cliente__razon_social', 'requerimiento__cliente__rut',
                 'requerimiento__planta__nombre', 'requerimiento__planta__region2', 'requerimiento__planta__ciudad2', 'requerimiento__planta__direccion', 'requerimiento__planta__gratificacion',
                 'trabajador__user__planta__nombre').order_by('trabajador__user__planta')


        context = super().get_context_data(**kwargs)

        context['datos'] = RequerimientoTrabajador.objects.filter(pk=requerimiento_trabajador_id).values(
                'trabajador', 'trabajador__first_name', 'trabajador__last_name', 'trabajador__rut','trabajador__estado_civil__nombre',
                'trabajador__fecha_nacimiento', 'trabajador__domicilio', 'trabajador__ciudad__nombre', 'trabajador__afp__nombre', 'trabajador__salud__nombre',
                'trabajador__nivel_estudio__nombre', 'trabajador__telefono', 'trabajador__nacionalidad__nombre', 'requerimiento__nombre',
                'referido', 'area_cargo__area__nombre', 'area_cargo__cargo__nombre', 'requerimiento__centro_costo', 'requerimiento__cliente__razon_social',
                'requerimiento__cliente__rut', 'requerimiento__codigo', 'requerimiento__planta__nombre', 'requerimiento__planta',
                'requerimiento__planta__region2__nombre', 'requerimiento__planta__provincia2__nombre','requerimiento__fecha_adendum','requerimiento__causal',
                'requerimiento__planta__ciudad2__nombre', 'requerimiento__planta__direccion','requerimiento__descripcion', 'requerimiento__fecha_inicio',
                'requerimiento__fecha_termino', 'requerimiento__planta__gratificacion__nombre','requerimiento__planta__gratificacion').order_by('trabajador__rut')
        context['contratos'] = Contrato.objects.filter(requerimiento_trabajador_id=requerimiento_trabajador_id, status=True ).values( 'id', 'valores_diario__valor_diario',
                'requerimiento_trabajador', 'estado_contrato','sueldo_base', 'tipo_documento__nombre','causal__nombre' ,'causal', 'motivo', 'fecha_inicio',
                 'fecha_termino', 'horario__nombre' , 'fecha_termino_ultimo_anexo', 'trabajador__first_name', 'trabajador__last_name', 'trabajador__domicilio', 'tipo_documento' )
        valores_diario__valor_diario = Contrato.objects.filter(requerimiento_trabajador_id=requerimiento_trabajador_id, status=True ).values( 'id', 'valores_diario__valor_diario')
        context['anexos'] = Anexo.objects.filter(requerimiento_trabajador_id=requerimiento_trabajador_id, status=True).values( 'id', 'estado_anexo',
                'requerimiento_trabajador', 'nueva_renta', 'contrato__tipo_documento__nombre','causal__nombre' ,'causal', 'motivo', 'fecha_inicio',
                 'fecha_termino' ).order_by('fecha_inicio')
        try:
            context['contrato'] = Contrato.objects.get(requerimiento_trabajador_id=requerimiento_trabajador_id)
            context['anexo'] = Anexo.objects.filter(requerimiento_trabajador_id=requerimiento_trabajador_id).latest()
            ultimo_anexo_contrato = Anexo.objects.values_list('estado_anexo', flat=True).filter(requerimiento_trabajador_id=requerimiento_trabajador_id, status=True).latest('id')
            id_ultimo_anexo = Anexo.objects.values_list('id', flat=True).filter(requerimiento_trabajador_id=requerimiento_trabajador_id, status=True).latest('id')
            # Trae el último anexo del contrato
            # ultimo_anexo_contrato = 'SI'
            context['ultimo_anexo_contrato'] = ultimo_anexo_contrato
            context['id_ultimo_anexo'] = id_ultimo_anexo
        except:
            # context['contrato'] = 0
            # context['anexo'] = 0
            # ultimo_anexo_contrato = 'NO'
            print('')
        
        ane = Anexo.objects.filter(requerimiento_trabajador_id=requerimiento_trabajador_id, status=True).exists()
        if(ane == True):
            anex = 'SI'
        # Finiquito
        contrato_diario = Contrato.objects.filter(requerimiento_trabajador_id=requerimiento_trabajador_id, tipo_documento__nombre='Contrato Diario', status=True ).exists()
        cantidadcontratos = 0
        ultimo2 = 0
        if(contrato_diario == True):
            # La fecha de inicio y la fecha de termino es la misma en contrato diario
            cantidadcontratos = Contrato.objects.filter(requerimiento_trabajador_id=requerimiento_trabajador_id, tipo_documento__nombre='Contrato Diario', status=True ).count()
            ultimo = Contrato.objects.filter(requerimiento_trabajador_id=requerimiento_trabajador_id).latest('id')
            try:
                ultimo_cd_aprob = Contrato.objects.filter(requerimiento_trabajador_id=requerimiento_trabajador_id, estado_contrato = 'AP').latest('id')
                context['ultimo_contrato_diario_aprob'] = ultimo_cd_aprob.id
            except:
                print('')

            context['ultimo_contrato'] = ultimo
            ultimo2 = ultimo.tipo_documento.id
            context['contador'] = cantidadcontratos
            inicio_termino = str(ultimo.fecha_termino)
            if (now.strftime("%Y-%m-%d") > inicio_termino):
                finiquito = 'SI'
        # finalizo_contrato = Contrato.objects.values_list('fin_requerimiento', flat=True).get(requerimiento_trabajador_id=requerimiento_trabajador_id, status=True).exclude(tipo_documento__nombre='Contrato Diario')
        finalizo_contrato = Contrato.objects.filter(requerimiento_trabajador_id=requerimiento_trabajador_id, status=True).exclude(tipo_documento__nombre='Contrato Diario').values('fin_requerimiento')
        if finalizo_contrato == None:
            fin_contrato = 'SI'
        bonos = RequerimientoTrabajador.objects.values_list('requerimiento__planta__bono', flat=True).filter(pk=requerimiento_trabajador_id)
        largobonos = len(bonos)
        fecha_restriccion = requer_trabajador.requerimiento.fecha_inicio
        try:
            contrato_fecha = Contrato.objects.filter(trabajador_id=requer_trabajador.trabajador.id, status=True ).latest('id')
            inicio_contrato = contrato_fecha.fecha_termino_ultimo_anexo
            if (inicio_contrato < requer_trabajador.requerimiento.fecha_inicio):
                fecha_restriccion = requer_trabajador.requerimiento.fecha_inicio
            else: 
                fecha_restriccion = inicio_contrato
        except:
            print('')
        

        context['fecha_restriccion'] =  fecha_restriccion        
        context['ultimo'] = ultimo2
        context['contador'] = cantidadcontratos
        context['anex'] = anex
        context['finiquito'] = finiquito
        context['fin_contrato'] = fin_contrato
        context['largobonos'] = largobonos
        context['requerimiento_trabajador_id'] = requerimiento_trabajador_id
        context['bonos'] = RequerimientoTrabajador.objects.filter(pk=requerimiento_trabajador_id).values('requerimiento__planta__bono','requerimiento__planta__bono__nombre')
        context['form3'] = RequeriTrabajadorForm(instance=requer_trabajador, user=trabaj)
        context['form2'] = ContratoForm(horario=requer_trabajador.requerimiento.cliente.horario.all())
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
        if self.request.user.groups.filter(name__in=['Administrador']).exists():
            context['contratos'] = Contrato.objects.all().order_by('modified')
                # created_by_id=self.request.user).order_by('modified')
        elif self.request.user.groups.filter(name__in=['Administrador Contratos', 'Psicologo']).exists():
            context['contratos'] = Contrato.objects.filter(
                created_by_id=self.request.user, planta__in=plantas, status=True).order_by('modified')
        else:
            # Obtengo todos los contratos por firmar de todas las plantas a las
            # que pertenece el usuario.
            context['contratos'] = Contrato.objects.filter(
                planta__in=plantas, estado_firma=Contrato.POR_FIRMAR, trabajador__user=self.request.user)
            context['result'] = Contrato.objects.values(
                'planta__nombre').order_by('planta')
                # 'planta__nombre').order_by('planta').annotate(count=Count(estado=Contrato.FIRMADO_TRABAJADOR))

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


class SolicitudContrato(TemplateView):
    template_name = 'contratos/solicitudes_pendientes_contrato.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Contrato.objects.filter(estado_contrato='PV', status=True):
                    data.append(i.toJSON())
            elif action == 'aprobar':
                revision = Revision.objects.get(contrato_id=request.POST['id'])
                revision.estado = 'AP'
                revision.save()
                contrato = Contrato.objects.get(pk=request.POST['id'])
                contrato.fecha_aprobacion  = datetime.now()
                contrato.estado_contrato = 'AP'
                contrato.save()
                finiquito(contrato.id)

                fecha_ingreso_trabajador_palabras = fecha_a_letras(contrato.fecha_inicio)
                send_mail(
                    'Nueva Solicitud en SGO3 | Contrato',
                    'Estimado(a) la solicitud de contrato para el trabajador ' + str(contrato.trabajador.first_name) +' '+str(contrato.trabajador.last_name)+' con fecha de ingreso: ' 
                    + str(fecha_ingreso_trabajador_palabras) + ' para la planta: '+ str(contrato.planta.nombre)+' ha sido APROBADA',
                    contrato.created_by.email,
                    ['contratos@empresasintegra.cl', 'soporte@empresasintegra.cl', contrato.created_by.email],
                    fail_silently=False,
                )

            elif action == 'rechazar':
                revision = Revision.objects.get(contrato_id=request.POST['id'])
                revision.estado = 'RC'
                revision.obs = request.POST['obs']
                revision.save()
                contrato = Contrato.objects.get(pk=request.POST['id'])
                url = contrato.archivo
                ruta_documentos = ContratosParametrosGen.objects.values_list('ruta_documentos', flat=True).get(pk=1, status=True)
                path = os.path.join(ruta_documentos)
                os.remove(path + str(url))
                contrato.archivo = None
                contrato.estado_contrato = 'RC'
                contrato.save()
                doc_contrato = DocumentosContrato.objects.get(contrato_id=request.POST['id'], tipo_documento_id = 14 )
                url2 = doc_contrato.archivo
                os.remove(path+ 'contratos\\' +str(url2))
                doc_contrato.delete()


                fecha_ingreso_trabajador_palabras = fecha_a_letras(contrato.fecha_inicio)
                send_mail(
                    'Nueva Solicitud en SGO3 | Contrato',
                    'Estimado(a) la solicitud de contrato para el trabajador ' + str(contrato.trabajador.first_name) +' '+str(contrato.trabajador.last_name)+' con fecha de ingreso: ' 
                    + str(fecha_ingreso_trabajador_palabras) + ' para la planta: '+ str(contrato.planta.nombre)+' ha sido RECHAZADO por el motivo: ' + str(request.POST['obs']),
                    contrato.created_by.email,
                    ['contratos@empresasintegra.cl', 'soporte@empresasintegra.cl', contrato.created_by.email],
                    fail_silently=False,
                )
            elif action == 'aprobacion_masiva':
                aprobacion =request.POST.getlist('check_aprobacion')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class BajaContrato(TemplateView):
    template_name = 'contratos/list_contrato_baja.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Baja.objects.filter(estado='PD', status=True, contrato__isnull=False):
                    data.append(i.toJSON())
            elif action == 'aprobar':
                baja = Baja.objects.get(pk=request.POST['id'])
                baja.estado = 'AP'
                baja.save()
                contrato = Contrato.objects.get(pk=request.POST['contrato_id'])
                contrato.fecha_aprobacion_baja  = datetime.now()
                contrato.estado_contrato = 'BJ'
                url = contrato.archivo
                ruta_documentos = ContratosParametrosGen.objects.values_list('ruta_documentos', flat=True).get(pk=1, status=True)
                path = os.path.join(ruta_documentos)
                os.remove(path+ '\\' +str(url))
                contrato.archivo = None
                contrato.status = False
                contrato.save()
                
                fecha_ingreso_trabajador_palabras = fecha_a_letras(contrato.fecha_inicio)
                send_mail(
                'Nueva Solicitud en SGO3 | Contrato',
                'Estimado(a) se ha APROBADO la solicitado de baja de contrato para el trabajador: ' + str(contrato.trabajador.first_name) +' '+str(contrato.trabajador.last_name)+' con fecha de ingreso: ' 
                + str(fecha_ingreso_trabajador_palabras) + ' para la planta: '+ str(contrato.planta.nombre) +'por el motivo ' + baja.motivo.nombre,
                contrato.created_by.email,
                ['contratos@empresasintegra.cl', 'soporte@empresasintegra.cl', contrato.created_by.email],
                fail_silently=False,
                    )
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class AnexoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
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
def create_anexo(request):
            requerimientotrabajador = request.POST['requerimiento_trabajador_id'] 
            anexo = Anexo()
            anexo.trabajador_id = request.POST['trabajador_id']
            anexo.requerimiento_trabajador_id = request.POST['requerimiento_trabajador_id']
            anexo.fecha_inicio = request.POST['UltimoAnexo']
            anexo.fecha_termino = request.POST['fechaTerminoAnexo']
            if "motivo" in request.POST:
                anexo.motivo = request.POST['NuevoMotivo']
            anexo.fecha_termino_anexo_anterior = request.POST['fechaTerminoAnexo']
            anexo.contrato_id = request.POST['id_contrato']
            if "renta" in request.POST:
                 anexo.nueva_renta = request.POST['NuevaRenta']
            anexo.causal_id = request.POST['id_causalanexo']
            anexo.planta_id = request.POST['planta']
            anexo.save()
            contrato = Contrato.objects.get(pk=request.POST['id_contrato'])
            contrato.fecha_termino_ultimo_anexo = request.POST['fechaTerminoAnexo']
            contrato.save()
            return redirect('contratos:create_contrato', requerimientotrabajador)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def aprobacion_masiva_anexo(request, aprobacion):
  
    lista_aprobacion = aprobacion.split(',')
    for i in lista_aprobacion:
        revision = Revision.objects.get(anexo_id=i)
        revision.estado = 'AP'
        revision.save()
        anexo = Anexo.objects.get(pk=i)
        anexo.fecha_aprobacion  = datetime.now()
        anexo.estado_anexo = 'AP'
        anexo.save()
    messages.success(request, 'Anexos aprobados Exitosamente')
    return redirect('contratos:solicitud-contrato',)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def update_anexo(request, anexo_id,template_name='contratos/anexo_update.html'):
            data = dict()
            anexo = get_object_or_404(Anexo, pk=anexo_id)
            contrato = get_object_or_404(Contrato, pk=anexo.contrato_id)

            
            try:
                revision = Revision.objects.get(anexo_id=anexo_id)
            except:
                 revision = ''

            if request.method == 'POST':
                anexo.fecha_termino = request.POST['fechaTerminoAnexo']
                if "NuevoMotivo1" in request.POST:
                    anexo.motivo = request.POST['NuevoMotivo1']
                elif "NuevoMotivo2" in request.POST :
                    anexo.motivo = request.POST['NuevoMotivo2']
                if 'NuevaRenta1' in request.POST and request.POST['NuevaRenta1'] != '' :
                    anexo.nueva_renta = request.POST['NuevaRenta1']
                elif 'NuevaRenta2' in request.POST and request.POST['NuevaRenta2'] != '' :
                    anexo.nueva_renta =  request.POST['NuevaRenta2']
                else:
                    anexo.nueva_renta =  None
                anexo.save()
                contrato.fecha_termino_ultimo_anexo = request.POST['fechaTerminoAnexo']
                contrato.save()
                return redirect('contratos:create_contrato',anexo.requerimiento_trabajador_id)
            else:
                contratos = Contrato.objects.all().filter(requerimiento_trabajador_id =anexo.requerimiento_trabajador_id, status=True ).values( 'id',
                'requerimiento_trabajador', 'estado_contrato','sueldo_base', 'tipo_documento__nombre','causal__nombre' ,'causal', 'motivo', 'fecha_inicio',
                'fecha_termino', 'horario__nombre' , 'fecha_termino_ultimo_anexo', 'requerimiento_trabajador__trabajador__first_name', 'requerimiento_trabajador__trabajador__last_name', 'requerimiento_trabajador__trabajador__domicilio' ).distinct()
                context={
                    'contratos' : contratos,
                    'anexo_id' : anexo.id,
                    'fecha_termino' : anexo.fecha_termino,
                    'motivo': anexo.motivo,
                    'nuevarenta': anexo.nueva_renta,
                    'revision' : revision
                }
                data['html_form'] = render_to_string(
                    template_name,
                    context,
                    request=request,
                )
                return JsonResponse(data)


@login_required
def delete_anexo(request, object_id, template_name='contratos/anexo_delete.html'):
    data = dict()
    object = get_object_or_404(Anexo, pk=object_id)
    # Si tiene último anexo
    # Sino, es el primer anexo
    pk = object.requerimiento_trabajador.id

    if request.method == 'POST':
        try:
            if Anexo.objects.filter(requerimiento_trabajador_id=pk, estado_anexo = 'AP').latest('id') == True:
                ultimo_anexo = Anexo.objects.filter(requerimiento_trabajador_id=pk, estado_anexo = 'AP').latest('id')
            else:
                ultimo_anexo = Anexo.objects.filter(requerimiento_trabajador_id=pk, estado_anexo = 'CR').latest('id')
            object.delete()
            messages.success(request, 'Anexo eliminado Exitosamente')
            actualizar = Contrato.objects.get(pk=ultimo_anexo.contrato.id)
            actualizar.fecha_termino_ultimo_anexo = ultimo_anexo.fecha_termino
            actualizar.save()
        except ProtectedError:
            messages.error(request, 'El anexo no se pudo eliminar.')
            return redirect('contratos:create_contrato', pk)

        return redirect('contratos:create_contrato', pk)

    context = {'object': object}
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request
    )
    return JsonResponse(data)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def enviar_revision_anexo(request, anexo_id):
    anexo = get_object_or_404(Anexo, pk=anexo_id)
    # Trae el id de la planta del Requerimiento
    plant_template = Contrato.objects.values_list('planta', flat=True).get(pk=anexo.contrato_id, status=True)
    # Busca si la planta tiene plantilla 
    if not Plantilla.objects.filter(plantas=plant_template, tipo_id=5).exists():
        messages.error(request, 'La Planta no posee Plantilla asociada. Por favor gestionar con el Dpto. de Contratos')
        return redirect('contratos:create_contrato', anexo.requerimiento_trabajador_id)

    else:
        anexo.estado_anexo = 'PV'
        anexo.fecha_solicitud = datetime.now()
        try:
            revision = Revision.objects.get(anexo_id=anexo_id)
            revision.estado = 'PD'
            revision.save()
        except:  
            revision = Revision()
            revision.anexo_id = anexo.id
            revision.save()
  
        # Trae la plantilla que tiene la planta
        formato = Plantilla.objects.values('archivo', 'abreviatura', 'tipo_id').filter(plantas=plant_template, tipo_id=5)
        for formt in formato:
            now = datetime.now()
            doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT + '/' + formt['archivo']))
            # Variables de Anexo
            context = { 'codigo_req': anexo.contrato.requerimiento_trabajador.requerimiento.codigo,
                        'comuna_planta': anexo.contrato.planta.ciudad2.nombre,
                        'fecha_contrato_anterior':fecha_a_letras(anexo.contrato.fecha_termino_ultimo_anexo),
                        'nombres_trabajador': anexo.contrato.trabajador.first_name,
                        'apellidos_trabajador': anexo.contrato.trabajador.last_name,
                        'rut_trabajador': anexo.contrato.trabajador.rut,
                        'nacionalidad': anexo.contrato.trabajador.nacionalidad.nombre,
                        'fecha_nacimiento': fecha_a_letras(anexo.contrato.trabajador.fecha_nacimiento),
                        'estado_civil': anexo.contrato.trabajador.estado_civil.nombre,
                        'domicilio_trabajador': anexo.contrato.trabajador.domicilio,
                        'comuna_trabajador': anexo.contrato.trabajador.ciudad.nombre,
                        'nuevo_parrafo': anexo.motivo,
                        'nueva_renta': anexo.contrato.nueva_renta,
                        
                        }
            rut_trabajador = anexo.contrato.trabajador.rut
            doc.render(context)
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

            # Contratos Parametros General, ruta_documentos donde guardara el documento
            ruta_documentos = ContratosParametrosGen.objects.values_list('ruta_documentos', flat=True).get(pk=1, status=True)
            path = os.path.join(ruta_documentos)
            # Si carpeta no existe, crea carpeta de contratos.
            carpeta = 'anexos'
            try:
                os.mkdir(path + carpeta)
                path = os.path.join(settings.MEDIA_ROOT + '/anexos/')
                doc.save(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(anexo_id) +'.docx')
                win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())     

                convert(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(anexo_id) + ".docx", path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(anexo_id) + ".pdf")
                        
                url = str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(anexo_id) + ".pdf"
                anexo.archivo = 'anexos/' + url
                anexo.save()
                # Elimino el documento word.
                os.remove(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(anexo_id) + '.docx')
                messages.success(request, 'Anexo enviado a revisión Exitosamente')
            except:
                path = os.path.join(settings.MEDIA_ROOT + '/anexos/')
                doc.save(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(anexo_id) +'.docx')
                win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())     

                convert(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(anexo_id) + ".docx", path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(anexo_id) + ".pdf")
                        
                url = str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(anexo_id) + ".pdf"
                anexo.archivo = 'anexos/' + url
                anexo.save()
                # Elimino el documento word.
                os.remove(path + str(rut_trabajador) + "_" + formt['abreviatura'] + "_" + str(anexo_id) + '.docx')
                messages.success(request, 'Anexo enviado a revisión Exitosamente')
    return redirect('contratos:create_contrato', anexo.requerimiento_trabajador_id)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def baja_contrato_anexo(request,anexo_id, template_name='contratos/baja_anexo.html'): 
    data = dict()

    anexo = get_object_or_404(Anexo, pk=anexo_id)
    if request.method == 'POST':
        anexo.estado_anexo = 'PB'
        anexo.fecha_solicitud_baja = datetime.now()
        anexo.save()
        baja = Baja()
        baja.anexo_id = anexo_id
        baja.motivo_id = request.POST['motivo']
        baja.save()
        messages.success(request, 'Anexo enviado a proceso de baja Exitosamente')
        return redirect('contratos:create_contrato', anexo.requerimiento_trabajador_id)

    else:
    
        context = {
            'form10': MotivoBajaForm,
            'anexo_id': anexo_id, 
            }
        data['html_form'] = render_to_string(
            template_name,
            context,
            request=request,
        )
        return JsonResponse(data)


@login_required
@permission_required('contratos.add_contrato', raise_exception=True)
def solicitudes_pendientes_anexo(request, anexo_id, template_name='contratos/anexo_pdf.html'):
    data = dict()
    anexo = get_object_or_404(Anexo, pk=anexo_id)

    context = {'anexo': anexo, }
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


@login_required
@permission_required('contratos.add_anexo', raise_exception=True)
def solicitudes_pendientes_anexo_baja(request, anexo_id, template_name='contratos/modal_baja_anexo.html'):
    data = dict()
    anexo = get_object_or_404(Anexo, pk=anexo_id)
    baja = get_object_or_404(Baja, anexo_id=anexo_id)


    context = {
        'anexo': anexo,
        'baja': baja
         }
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


class SolicitudAnexo(TemplateView):
    template_name = 'contratos/solicitudes_pendientes_anexo.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Anexo.objects.filter(estado_anexo='PV', status=True):
                    data.append(i.toJSON())
            elif action == 'aprobar':
                revision = Revision.objects.get(anexo_id=request.POST['id'])
                revision.estado = 'AP'
                revision.save()
                anexo = Anexo.objects.get(pk=request.POST['id'])
                anexo.fecha_aprobacion  = datetime.now()
                anexo.estado_anexo = 'AP'
                anexo.save()
            elif action == 'rechazar':
                revision = Revision.objects.get(anexo_id=request.POST['id'])
                revision.estado = 'RC'
                revision.obs = request.POST['obs']
                revision.save()
                anexo = Anexo.objects.get(pk=request.POST['id'])
                url = anexo.archivo
                os.remove(str(url))
                anexo.archivo = None
                anexo.estado_anexo = 'RC'
                anexo.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class AnexoCompletaListView(ListView):
    model = Anexo
    form_class = CompletasForm
    template_name = 'contratos/consulta_completas_anexos.html'
    
    
    def get_queryset(self):
        return Anexo.objects.filter(estado_anexo='AP', fecha_inicio__month=str(now.month), status=True)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['form'] = CompletasForm(instance=Anexo)
        context ['data'] = Anexo.objects.filter(estado_anexo='AP', fecha_inicio__month=str(now.month), status=True)
        return context

def buscar_anexo(request):
    if request.method == 'POST':
        planta = request.POST.get('planta')
        mes = request.POST.get('mes')
        if mes:
            data = Anexo.objects.filter(estado_anexo='AP', planta_id=planta, fecha_inicio__month=mes, status=True)
            context = {'data': data}
            context ['form'] = CompletasForm(instance=Anexo)
            return render(request, 'contratos/consulta_completas_anexos.html', context)
        else:
            data = Anexo.objects.filter(estado_anexo='AP', planta_id=planta, status=True)
            context = {'data': data}
            context ['form'] = CompletasForm(instance=Anexo)
            return render(request, 'contratos/consulta_completas_anexos.html', context)


class BajaAnexo(TemplateView):
    template_name = 'contratos/list_anexo_baja.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Baja.objects.filter(estado='PD', status=True, anexo__isnull=False):
                    data.append(i.toJSON())
            elif action == 'aprobar':
                baja = Baja.objects.get(pk=request.POST['id'])
                baja.estado = 'AP'
                baja.save()
                anexo = Anexo.objects.get(pk=request.POST['contrato_id'])
                anexo.fecha_aprobacion_baja  = datetime.now()
                anexo.estado_anexo = 'BJ'
                url = anexo.archivo
                os.remove(str(url))
                anexo.archivo = None
                anexo.status = False
                anexo.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class AnexoBajaListView(ListView):
    model = Anexo
    form_class = CompletasForm
    template_name = 'contratos/consulta_bajas_anexos.html'
    
    
    def get_queryset(self):
        return Anexo.objects.filter(estado_anexo='BJ', fecha_inicio__month=str(now.month), status=True)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['form'] = CompletasForm(instance=Anexo)
        context ['data'] = Anexo.objects.filter(estado_anexo='BJ', fecha_inicio__month=str(now.month), status=True)
        return context

def buscar_baja_anexo(request):
    if request.method == 'POST':
        planta = request.POST.get('planta')
        mes = request.POST.get('mes')
        if mes:
            data = Anexo.objects.filter(estado_anexo='BJ', planta_id=planta, fecha_inicio__month=mes, status=True)
            context = {'data': data}
            context ['form'] = CompletasForm(instance=Anexo)
            return render(request, 'contratos/consulta_bajas_anexos.html', context)
        else:
            data = Anexo.objects.filter(estado_anexo='BJ', planta_id=planta, status=True)
            context = {'data': data}
            context ['form'] = CompletasForm(instance=Anexo)
            return render(request, 'contratos/consulta_bajas_anexos.html', context)


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
            uidb64 = "1s72q4rgru5hyt6fyrjhvc8y1a73piq6"
            token = "oN8ZslfdNk6n6sjUKo63roxbVdfeRHGQthkT48CjlTB57IPj2tn1Ga6d7VRMOGlF"

            if request.method == 'POST':
                print()

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
