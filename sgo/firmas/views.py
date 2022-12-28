# Create your views here.
"""Firmas  Views."""

import os
import base64
from base64 import b64decode
import requests
import json 
import sys
from datetime import date, datetime
from queue import Empty
import threading
import time
# Django
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
# Model
from contratos.models import Contrato, DocumentosContrato, Anexo, ContratosParametrosGen
from firmas.models import Firma


# # Tarea a ejecutarse cada determinado tiempo.
# def timer():
#     while True:
#         print("¡Hola, mundito!")
#         time.sleep(3600)   # 3600 segundos es 1 hr.
# # Iniciar la ejecución en segundo plano.
# t = threading.Thread(target=timer)
# t.start()


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
                
                url = "https://empresasintegra.evicertia.com/api/EviSign/Submit"

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
                                        "Key": "RequireContentCommitment", "Value": False
                                    }
                                    # {
                                    #     "Key": "RequireContentCommitmentOrder", "Value": orden
                                    # }
                                ]
                            })
                except Exception as e:
                    data['error'] = str(e)

                payload = json.dumps({
                "Subject": "Prueba Firma Contrato",
                "Document": document,
                "Attachments": 
                    doc_contrato,
                "SigningParties": [
                    {
                        "name": contrato.trabajador.first_name + ' ' + contrato.trabajador.last_name,
                        "address": contrato.trabajador.email,
                        "signingMethod": "Email Pin",
                        "role": "Signer",
                        "signingOrder": 1,
                        "legalName": "Trabajador"
                    },
                    {
                        "name": "Empresas Integra Ltda.",
                        "address": "firma@empresasintegra.cl",
                        "signingMethod": "WebClick",
                        "role": "Signer",
                        "signingOrder": 2,
                        "legalName": "Empleador"
                    }
                ],
                "Options": {
                    "TimeToLive": 4320,
                    "NumberOfReminders":3,
                    "notaryRetentionPeriod": 0,
                    "onlineRetentionPeriod": 2,
                    "language": "es-ES",
                    "EvidenceAccessControlMethod": "Public",
                    "CertificationLevel": "Advanced",

                    "RequireCaptcha": False
                },
                "Issuer": "EVISA"
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': 'Basic ZmlybWFAZW1wcmVzYXNpbnRlZ3JhLmNsOktGeFcwMkREMyM=',
                    'Cookie': 'X-UAId=1237; ss-id=kEDBUDCvtQL/m68MmIoY; ss-pid=fogDX+U1tusPTqHrA4eF'
                            }

                response = requests.request("POST", url, headers=headers, data=payload)

                print('API', response.text)
                print('Status Code', response.status_code)
                if response.status_code == 200:
                    contrato = Contrato.objects.get(pk=request.POST['id'])
                    contrato.estado_firma = 'EF'
                    contrato.obs = response.text
                    contrato.save()
                    api = Firma()
                    api.respuesta_api = response.text
                    # request.POST['nombre'].lower()
                    api.rut_trabajador = contrato.trabajador.rut
                    api.estado_firma_id = 1
                    api.contrato_id = contrato.id
                    api.status = True
                    api.save()
                    # contrato = Firma.objects.get(pk=request.POST['id'])
                    # contrato.estado_firma = 'EF'
                    # contrato.obs = response.text
                    # contrato.save()

                    # exit()
                    print('status_code 200')
                    messages.success(request, 'Enviado a Firma')
                elif response.status_code == 401:
                    print('status_code 401')
                    messages.error(request, 'Credenciales no válidas.')
                elif response.status_code == 403:
                    print('status_code 403')
                    messages.error(request, 'Sin Permisos.')
                elif response.status_code == 404:
                    print('status_code 404')
                    messages.error(request, 'No Encontrado.')
                elif response.status_code == 500:
                    print('status_code 500')
                    messages.error(request, 'Error del Servidor.')
                else:
                    print('=( algo malo paso')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class ContratoEnviadoList(TemplateView):
    template_name = 'contratos/contrato_enviado_list.html'

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
                # for i in Contrato.objects.filter(estado_contrato='AP', status=True):
                for i in Contrato.objects.filter(status=True).exclude(estado_firma="PF"):

                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # context = {'response': response.text, }
        # data = context,
        request=request
        return JsonResponse(data, safe=False)


@login_required
@permission_required('firmas.view_firma', raise_exception=True)
def firma_estado(request, contrato_id, template_name='firmas/estado_api.html'):
    """Estado de firma view."""

    firmado = get_object_or_404(Firma, contrato=contrato_id)
    api = firmado.respuesta_api
    uniqueid = api[13:-2]

    # Inicio integración de la API
    URL = "https://empresasintegra.evicertia.com/api/EviSign/Query"
    
    # Definiendo los parámetros y asignación del valor
    withUniqueIds = uniqueid
    includeAttachmentsOnResult = True
    includeAttachmentBlobsOnResult = True
    includeEventsOnResult = True
    includeAffidavitsOnResult = True
    includeAffidavitBlobsOnResult = True

    HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Basic ZmlybWFAZW1wcmVzYXNpbnRlZ3JhLmNsOktGeFcwMkREMyM=',
        'Cookie': 'X-UAId=1237; ss-id=kEDBUDCvtQL/m68MmIoY; ss-pid=fogDX+U1tusPTqHrA4eF'
        }
    
    #  Parámetros que se envian a la API
    PARAMS = {'withUniqueIds':withUniqueIds,
              'includeAttachmentsOnResult':includeAttachmentsOnResult,
              'includeAttachmentBlobsOnResult':includeAttachmentBlobsOnResult,
              'includeEventsOnResult':includeEventsOnResult,
              'includeAffidavitsOnResult':includeAffidavitsOnResult,
              'includeAffidavitBlobsOnResult':includeAffidavitBlobsOnResult
              }
    
    # Enviando una solicitud de obtención y guardando la respuesta como objeto de respuesta
    response = requests.get(url = URL, headers = HEADERS, params = PARAMS)
    # print('URL: ', response.url)
    # print('API', response.text)
    
    if response.status_code == 200:
        # Extrayendo datos en formato json
        data = response.json()
        # print(response.content)
        # print(response.text)

        # Actualiza el estado de la firma en Contratos
        contrato = Contrato.objects.get(pk=contrato_id)
        if data['results'][0]['outcome'] == 'None' and data['results'][0]['state'] == 'Processed':
            # ENVIADO_FIRMAR
            contrato.estado_firma = 'EF'

        elif data['results'][0]['outcome'] == 'None' and data['results'][0]['state'] == 'Sent':
            # FIRMADO_TRABAJADOR
            contrato.estado_firma = 'FT'

        elif data['results'][0]['outcome'] == 'Signed':
            # FIRMADO
            contrato.estado_firma = 'FF'

            # Actualiza el documento firmado (Contratos)
            docum = Contrato.objects.get(pk=contrato_id)
            # Elimino el documento sin firma.
            path = os.path.join(settings.MEDIA_ROOT)
            archivo = docum.archivo
            print('archivo', archivo)
            ruta = path + '/' + str(archivo)
            os.remove(ruta)
            print('se elimino archivo')
            # Definir la cadena Base64 del archivo PDF
            b64 = data['results'][0]['affidavits'][6]['bytes']
            # Decodifica la cadena Base64, asegurándote de que solo contenga caracteres válidos
            bytes = b64decode(b64, validate=True)
            # Realice una validación básica para asegurarse de que el resultado sea un archivo PDF válido
            if bytes[0:4] != b'%PDF':
                raise ValueError('Falta la firma del archivo PDF')
            # Escribir el contenido del PDF en un archivo local
            f = open(ruta, 'wb')
            f.write(bytes)
            f.close()
            # Se guarda el documento firmado
            doc_contrato = DocumentosContrato()
            doc_contrato.contrato_id = contrato_id
            doc_contrato.archivo = archivo
            doc_contrato.tipo_documento_id = 1
            doc_contrato.save()
            context = {'base64contrato': b64}

        elif data['results'][0]['outcome'] == 'Rejected':
            # OBJETADO
            contrato.estado_firma = 'OB'

        elif data['results'][0]['outcome'] == 'Expired':
            # EXPIRADO
            contrato.estado_firma = 'EX'
        contrato.save()

        # Actualiza el estado de la firma
        api = Firma.objects.get(contrato=contrato_id)
        if data['results'][0]['outcome'] == 'None' and data['results'][0]['state'] == 'Processed':
            # ENVIADO PENDIENTE
            api.estado_firma_id = 1
        elif data['results'][0]['outcome'] == 'None' and data['results'][0]['state'] == 'Sent':
            # FIRMADO TRABAJADOR
            api.estado_firma_id = 2
        elif data['results'][0]['outcome'] == 'Signed':
            # FIRMADO
            api.estado_firma_id = 3
        elif data['results'][0]['outcome'] == 'Rejected':
            # OBJETADO
            api.estado_firma_id = 4
        elif data['results'][0]['outcome'] == 'Expired':
            # EXPIRADO
            api.estado_firma_id = 5
        api.save()

        # if data['results'][0]['affidavits'][3]['bytes'] == None:
        #     base64 = data['results'][0]['affidavits'][3]['bytes']
        #     print('Tiene documento firmado')
        #     # Actualiza el documento firmado (Contratos)
        #     docum = Contrato.objects.get(pk=contrato_id)
        #     # Elimino el documento sin firma.
        #     path = os.path.join(settings.MEDIA_ROOT)
        #     archivo = docum.archivo
        #     os.remove(path + archivo)
            
        #     print('se elimino archivo')
        #     docum.archivo
        # else:
        #     base64 = data['results'][0]['affidavits'][0]['bytes']
        #     print('No tiene documento firmado')


        context = {'data': data,
                'results': data['results'][0],
                'signingPartiesE': data['results'][0]['signingParties'][0],
                'signingPartiesT': data['results'][0]['signingParties'][1],
                'affidavits': data['results'][0]['affidavits'][0],
                'attachments': data['results'][0]['attachments'][0],
                'signaturesE': data['results'][0]['signatures'][0],
                'signaturesT': data['results'][0]['signatures'][1],
                'signingMethod': data['results'][0]['signingParties'][0]['signingMethod'],
                'estado': firmado,
        }
        
        print('status_code 200')
        messages.success(request, 'Enviado a Firma')
    elif response.status_code == 401:
        print('status_code 401')
        messages.error(request, 'Credenciales no válidas.')
    elif response.status_code == 403:
        print('status_code 403')
        messages.error(request, 'Sin Permisos.')
    elif response.status_code == 404:
        print('status_code 404')
        messages.error(request, 'No Encontrado.')
    elif response.status_code == 500:
        print('status_code 500')
        messages.error(request, 'Error del Servidor.')
    else:
        print('=( algo malo paso')
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


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
                
                url = "https://empresasintegra.evicertia.com/api/EviSign/Submit"

                payload = json.dumps({
                "Subject": "Prueba Firma Anexo",
                "Document": document,
                "signingParties": [
                    {
                        "name": anexo.trabajador.first_name + ' ' + anexo.trabajador.last_name,
                        "address": anexo.trabajador.email,
                        "signingMethod": "Email Pin",
                        "role": "Signer",
                        "signingOrder": 1,
                        "legalName": "Trabajador"
                    },
                    {
                        "name": "Empresas Integra Ltda.",
                        "address": "firma@empresasintegra.cl",
                        "signingMethod": "WebClick",
                        "role": "Signer",
                        "signingOrder": 2,
                        "legalName": "Empleador"
                    }
                ],
                "Options": {
                    "timeToLive": 4320,
                    "NumberOfReminders":3,
                    "notaryRetentionPeriod": 0,
                    "onlineRetentionPeriod": 2,
                    "language": "es-ES",
                    "EvidenceAccessControlMethod": "Public",
                    "CertificationLevel": "Advanced",

                    "RequireCaptcha": False,
                },
                "Issuer": "EVISA"
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': 'Basic ZmlybWFAZW1wcmVzYXNpbnRlZ3JhLmNsOktGeFcwMkREMyM=',
                    'Cookie': 'X-UAId=1237; ss-id=kEDBUDCvtQL/m68MmIoY; ss-pid=fogDX+U1tusPTqHrA4eF'
                            }

                response = requests.request("POST", url, headers=headers, data=payload)

                print('API', response.text)
                if response.status_code == 200:
                    anexo = Anexo.objects.get(pk=request.POST['id'])
                    anexo.estado_firma = 'EF'
                    anexo.obs = response.text
                    anexo.save()
                    api = Firma()
                    api.respuesta_api = response.text
                    api.rut_trabajador = anexo.trabajador.rut
                    api.estado_firma_id = 1
                    api.anexo_id = anexo.id
                    api.status = True
                    api.save()
                    print('status_code 200')
                    messages.success(request, 'Enviado a Firma')
                elif response.status_code == 401:
                    print('status_code 401')
                    messages.error(request, 'Credenciales no válidas.')
                elif response.status_code == 403:
                    print('status_code 403')
                    messages.error(request, 'Sin Permisos.')
                elif response.status_code == 404:
                    print('status_code 404')
                    messages.error(request, 'No Encontrado.')
                elif response.status_code == 500:
                    print('status_code 500')
                    messages.error(request, 'Error del Servidor.')
                else:
                    print('=( algo malo paso')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class AnexoEnviadoList(TemplateView):
    template_name = 'contratos/anexo_enviado_list.html'

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
                # for i in Anexo.objects.filter(estado_anexo='AP', estado_firma='EF', status=True):
                for i in Anexo.objects.filter(status=True).exclude(estado_firma="PF"):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


@login_required
@permission_required('firmas.view_firma', raise_exception=True)
def estado_anexo(request, anexo_id, template_name='firmas/estado_api.html'):
    """Estado de firma view."""

    firmado = get_object_or_404(Firma, anexo=anexo_id)
    api = firmado.respuesta_api
    uniqueid = api[13:-2]
                
    # Inicio integración de la API

    URL = "https://empresasintegra.evicertia.com/api/EviSign/Query"
    
    # Definiendo los parámetros y asignación del valor
    withUniqueIds = uniqueid
    includeAttachmentsOnResult = True
    includeAttachmentBlobsOnResult = True
    includeEventsOnResult = True
    includeAffidavitsOnResult = True
    includeAffidavitBlobsOnResult = True

    HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Basic ZmlybWFAZW1wcmVzYXNpbnRlZ3JhLmNsOktGeFcwMkREMyM=',
        'Cookie': 'X-UAId=1237; ss-id=kEDBUDCvtQL/m68MmIoY; ss-pid=fogDX+U1tusPTqHrA4eF'
        }
    
    #  Parámetros que se envian a la API
    PARAMS = {'withUniqueIds':withUniqueIds,
              'includeAttachmentsOnResult':includeAttachmentsOnResult,
              'includeAttachmentBlobsOnResult':includeAttachmentBlobsOnResult,
              'includeEventsOnResult':includeEventsOnResult,
              'includeAffidavitsOnResult':includeAffidavitsOnResult,
              'includeAffidavitBlobsOnResult':includeAffidavitBlobsOnResult
              }
    
    # Enviando una solicitud de obtención y guardando la respuesta como objeto de respuesta
    response = requests.get(url = URL, headers = HEADERS, params = PARAMS)
    # print('URL: ', response.url)
    print('API', response.status_code)
    
    if response.status_code == 200:
        # Extrayendo datos en formato json
        data = response.json()
        # print(response.content)
        # print(response.text)

        # Actualiza el estado de la firma en el Anexo de contratos
        anex = Anexo.objects.get(pk=anexo_id)
        if data['results'][0]['outcome'] == 'None' and data['results'][0]['state'] == 'Processed':
            # ENVIADO_FIRMAR
            anex.estado_firma = 'EF'

        elif data['results'][0]['outcome'] == 'None' and data['results'][0]['state'] == 'Sent':
            # FIRMADO_TRABAJADOR
            anex.estado_firma = 'FT'

        elif data['results'][0]['outcome'] == 'Signed':
            # FIRMADO
            anex.estado_firma = 'FF'

            # Actualiza el documento firmado (Anexo)
            docum = Anexo.objects.get(pk=anexo_id)
            # Elimino el documento sin firma.
            path = os.path.join(settings.MEDIA_ROOT)
            archivo = docum.archivo
            print('archivo', archivo)
            ruta = path + '/' + str(archivo)
            os.remove(ruta)
            print('se elimino archivo')
            # Definir la cadena Base64 del archivo PDF
            b64 = data['results'][0]['affidavits'][6]['bytes']
            # Decodifica la cadena Base64, asegurándote de que solo contenga caracteres válidos
            bytes = b64decode(b64, validate=True)
            # Realice una validación básica para asegurarse de que el resultado sea un archivo PDF válido
            if bytes[0:4] != b'%PDF':
                raise ValueError('Falta la firma del archivo PDF')
            # Escribir el contenido del PDF en un archivo local
            f = open(ruta, 'wb')
            f.write(bytes)
            f.close()
            # Se guarda el documento firmado
            doc_contrato = DocumentosContrato()
            doc_contrato.contrato_id = anex.contrato_id
            doc_contrato.archivo = archivo
            doc_contrato.tipo_documento_id = 5
            doc_contrato.save()
            context = {'base64contrato': b64}

        elif data['results'][0]['outcome'] == 'Rejected':
            # OBJETADO
            anex.estado_firma = 'OB'

        elif data['results'][0]['outcome'] == 'Expired':
            # EXPIRADO
            anex.estado_firma = 'EX'
        anex.save()

        # Actualiza el estado de la firma
        api = Firma.objects.get(anexo=anexo_id)
        if data['results'][0]['outcome'] == 'None' and data['results'][0]['state'] == 'Processed':
            # ENVIADO PENDIENTE
            api.estado_firma_id = 1
        elif data['results'][0]['outcome'] == 'None' and data['results'][0]['state'] == 'Sent':
            # FIRMADO TRABAJADOR
            api.estado_firma_id = 2
        elif data['results'][0]['outcome'] == 'Signed':
            # FIRMADO
            api.estado_firma_id = 3
            api.fecha_firma = data['results'][0]['signedOn']
        elif data['results'][0]['outcome'] == 'Rejected':
            # OBJETADO
            api.estado_firma_id = 4
        elif data['results'][0]['outcome'] == 'Expired':
            # EXPIRADO
            api.estado_firma_id = 5
        api.save()


        context = {'data': data,
                'results': data['results'][0],
                'signingPartiesE': data['results'][0]['signingParties'][0],
                'signingPartiesT': data['results'][0]['signingParties'][1],
                'affidavits': data['results'][0]['affidavits'][0],
                'signaturesE': data['results'][0]['signatures'][0],
                'signaturesT': data['results'][0]['signatures'][1],
                'signingMethod': data['results'][0]['signingParties'][0]['signingMethod'],
                'estado': firmado,
        }
        print('status_code 200')
        messages.success(request, 'Enviado a Firma')
    elif response.status_code == 401:
        print('status_code 401')
        messages.error(request, 'Credenciales no válidas.')
    elif response.status_code == 403:
        print('status_code 403')
        messages.error(request, 'Sin Permisos.')
    elif response.status_code == 404:
        print('status_code 404')
        messages.error(request, 'No Encontrado.')
    elif response.status_code == 500:
        print('status_code 500')
        messages.error(request, 'Error del Servidor.')
    else:
        print('=( algo malo paso')
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)


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
