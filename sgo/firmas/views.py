# Create your views here.
"""Firmas  Views."""

import os
import base64
import requests
import json 
import sys
from datetime import date, datetime
from queue import Empty
# Django
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView
from django.http import Http404, JsonResponse
# Model
from contratos.models import Contrato, DocumentosContrato, Anexo, ContratosParametrosGen
from firmas.models import Firma


class ContratoAprobadoList(TemplateView):
    template_name = 'contratos/contrato_aprobado_list.html'

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
                for i in Contrato.objects.filter(estado_contrato='AP', estado_firma='PF', status=True):
                    data.append(i.toJSON())
            elif action == 'aprobar':
                # Inicio integración de la API
                contrato = Contrato.objects.get(pk=request.POST['id'])
                parametro_general = ContratosParametrosGen.objects.values_list('ruta_documentos', flat=True).get(pk=1)
                nombre_archivo = Contrato.objects.values_list('archivo', flat=True).get(pk=request.POST['id'])
                ubicacion = parametro_general + nombre_archivo
                with open(ubicacion, "rb") as pdf_file:
                    documento = base64.b64encode(pdf_file.read()).decode('utf-8')
                document = f'{documento}'
                
                url = "https://app.ecertia.com/api/EviSign/Submit"

                doc_adicionales = DocumentosContrato.objects.filter(contrato_id  = request.POST['id'])
                data = {}
                try:
                    if not doc_adicionales == Empty:
                        data = []
                        doc_contrato = []
                        orden = 0
                        for i in DocumentosContrato.objects.filter(contrato_id  = request.POST['id']):
                            orden = orden + 1
                            nombre = str(i.archivo).split("\\")
                            nombre_pdf = nombre[-1]
                            da_archivo = parametro_general + str(i.archivo)
                            with open(da_archivo, "rb") as pdf_file:
                                documento_ad = base64.b64encode(pdf_file.read()).decode('utf-8')
                            doc_ad_base64 = f'{documento_ad}'
                            # exit()
                                
                            doc_contrato.append({
                                "Filename": nombre_pdf,
                                "MimeType": "application/pdf",
                                "Data": doc_ad_base64,
                                "attributes": [
                                    {
                                        "Key": "RequireContentCommitment", "Value": True
                                    },
                                    {
                                        "Key": "RequireContentCommitmentOrder", "Value": orden
                                    }
                                ]
                            })
                except Exception as e:
                    data['error'] = str(e)

                payload = json.dumps({
                "Subject": "Prueba Firma Contrato",
                "Document": document,
                "Attachments": 
                    doc_contrato,
                "SigningParties": {
                    "Name": contrato.trabajador.first_name + ' ' + contrato.trabajador.last_name,
                    "Address": contrato.trabajador.email,
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
                contrato = Contrato.objects.get(pk=request.POST['id'])
                contrato.estado_firma = 'EF'
                contrato.obs = response.text
                contrato.save()
                api = Firma()
                api.respuesta_api = response.text
                # request.POST['nombre'].lower()
                api.rut_trabajador = contrato.trabajador.rut
                api.estado_firma_id = 1
                api.status = True
                api.save()
                # contrato = Firma.objects.get(pk=request.POST['id'])
                # contrato.estado_firma = 'EF'
                # contrato.obs = response.text
                # contrato.save()

                # exit()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class ContratoEnviadoList(TemplateView):
    template_name = 'contratos/contrato_aprobado_list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # "PushNotificationUrl": "https://putsreq.com/QatBxyrqPOlHoMOZhi3S",
    # "PushNotificationFilter": ["Processed", "Sent", "Delivered", "Signed", "Rejected", "FullySigned", "Closed"]


    def post(self, request):

        # url = "https://totalsoft-test.ecertia.com/api/EviSign/Query?withUniqueIds=0183895c-349c-4068-8f1b-a32517dc9668&includeAttachmentsOnResult=true&includeAttachmentBlobsOnResult=true&includeEventsOnResult=true&includeAffidavitsOnResult=true&includeAffidavitBlobsOnResult=true"

        # payload = ""
        # headers = {
        # 'Accept': 'application/json',
        # 'Content-Type': 'application/json',
        # 'Authorization': 'Basic bWF5ZXJseW4ucm9kcmlndWV6QGVtcHJlc2FzaW50ZWdyYS5jbDppbnRlZ3JhNzYyNQ==',
        # 'Cookie': 'X-UAId=1237; ss-id=kEDBUDCvtQL/m68MmIoY; ss-pid=fogDX+U1tusPTqHrA4eF'
        # }

        # response = requests.request("GET", url, headers=headers, data=payload)

        # resp = (response.text)
        # print(response.text)


        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Contrato.objects.filter(estado_contrato='AP', estado_firma='EF', status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # context = {'response': response.text, }
        # data = context,
        request=request
        return JsonResponse(data, safe=False)


class AnexoAprobadoList(TemplateView):
    template_name = 'contratos/anexo_aprobado_list.html'

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
                for i in Anexo.objects.filter(estado_anexo='AP', estado_firma='PF', status=True):
                    data.append(i.toJSON())
            elif action == 'aprobar':
                # Inicio integración de la API
                anexo = Anexo.objects.get(pk=request.POST['id'])
                parametro_general = ContratosParametrosGen.objects.values_list('ruta_documentos', flat=True).get(pk=1)
                nombre_archivo = Anexo.objects.values_list('archivo', flat=True).get(pk=request.POST['id'])
                ubicacion = parametro_general + nombre_archivo
                with open(ubicacion, "rb") as pdf_file:
                    documento = base64.b64encode(pdf_file.read()).decode('utf-8')
                document = f'{documento}'
                
                url = "https://app.ecertia.com/api/EviSign/Submit"

                payload = json.dumps({
                "Subject": "Prueba Firma Anexo",
                "Document": document,
                "SigningParties": {
                    "Name": anexo.trabajador.first_name + ' ' + anexo.trabajador.last_name,
                    "Address": anexo.trabajador.email,
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
                anexo = Anexo.objects.get(pk=request.POST['id'])
                anexo.estado_firma = 'EF'
                anexo.obs = response.text
                anexo.save()
                api = Firma()
                api.respuesta_api = response.text
                api.rut_trabajador = anexo.trabajador.rut
                api.estado_firma_id = 1
                api.status = True
                api.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class AnexoEnviadoList(TemplateView):
    template_name = 'contratos/anexo_aprobado_list.html'

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
                for i in Anexo.objects.filter(estado_anexo='AP', estado_firma='EF', status=True):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class ContratoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Firma List
    Vista para listar todos los firma según el usuario y sus las plantas
    relacionadas.
    """
    model = Contrato
    template_name = "contratos/contrato_aprobado_list.html"
    paginate_by = 25
    ordering = ['modified', ]

    permission_required = 'firmas.view_firma'
    raise_exception = True

    def get_queryset(self):
        search = self.request.GET.get('q')
        planta = self.kwargs.get('planta_id', None)

        if planta == '':
            planta = None

        if search:
            # Si el usuario no se administrador se despliegan los firmas en estado status
            # de las plantas a las que pertenece el usuario, según el critero de busqueda.
            if not self.request.user.groups.filter(name__in=['Administrador', ]).exists():
                queryset = super(ContratoListView, self).get_queryset().filter(
                    Q(status=True),
                    Q(plantas__in=self.request.user.planta.all()),
                    Q(nombre__icontains=search)
                ).distinct()
            else:
                # Si el usuario es administrador se despliegan todos los firmas
                # segun el critero de busqueda.
                queryset = super(ContratoListView, self).get_queryset().filter(
                    Q(nombre__icontains=search)
                ).distinct()
        else:
            # Si el usuario no es administrador, se despliegan los firmas en estado
            # status de las plantas a las que pertenece el usuario.
            if not self.request.user.groups.filter(name__in=['Administrador']).exists():
                queryset = super(ContratoListView, self).get_queryset().filter(
                    Q(status=True),
                    Q(plantas__in=self.request.user.planta.all())
                ).distinct()
            else:
                # Si el usuario es administrador, se despliegan todos los firmas.
                if planta is None:
                    queryset = super(ContratoListView, self).get_queryset()
                else:
                    # Si recibe la planta, solo muestra los firmas que pertenecen a esa planta.
                    queryset = super(ContratoListView, self).get_queryset().filter(
                        Q(plantas=planta)
                    ).distinct()

        return queryset
