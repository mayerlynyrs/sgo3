from django.shortcuts import render

# Create your views here.
"""Firmas  Views."""

import os
import base64
import requests
import json
from datetime import date, datetime
# Django
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView
from django.http import Http404, JsonResponse
# Model
from contratos.models import Contrato
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
                for i in Contrato.objects.filter(estado_contrato='AP', status=True):
                    data.append(i.toJSON())
            elif action == 'aprobar':
                # Variables para la API
                contrato = Contrato.objects.get(pk=request.POST['id'])
                nombre_archivo = Contrato.objects.values_list('archivo', flat=True).get(pk=request.POST['id'])
                print('nombre archivo ', contrato.archivo)
                # exit()
                with open(nombre_archivo, "rb") as pdf_file:
                    documento = base64.b64encode(pdf_file.read()).decode('utf-8')
                document = f'{documento}'
                # print('document ', document)
                
                url = "https://app.ecertia.com/api/EviSign/Submit"

                payload = json.dumps({
                "Subject": "Prueba Firma Contrato",
                "Document": document,
                "Attachments": [
                    {
                        "Filename": "attach1.pdf",
                        "MimeType": "application/pdf",
                        "Data": "JVBERi0xLjEKJcKlwrHDqwoKMSAwIG9iagogIDw8IC9UeXBlIC9DYXRhbG9nCiAgICAgL1BhZ2VzIDIgMCBSCiAgPj4KZW5kb2JqCgoyIDAgb2JqCiAgPDwgL1R5cGUgL1BhZ2VzCiAgICAgL0tpZHMgWzMgMCBSXQogICAgIC9Db3VudCAxCiAgICAgL01lZGlhQm94IFswIDAgNTk1IDgyMl0KICA+PgplbmRvYmoKCjMgMCBvYmoKICA8PCAgL1R5cGUgL1BhZ2UKICAgICAgL1BhcmVudCAyIDAgUgogICAgICAvUmVzb3VyY2VzCiAgICAgICA8PCAvRm9udAogICAgICAgICAgIDw8IC9GMQogICAgICAgICAgICAgICA8PCAvVHlwZSAvRm9udAogICAgICAgICAgICAgICAgICAvU3VidHlwZSAvVHlwZTEKICAgICAgICAgICAgICAgICAgL0Jhc2VGb250IC9UaW1lcy1Sb21hbgogICAgICAgICAgICAgICA+PgogICAgICAgICAgID4+CiAgICAgICA+PgogICAgICAvQ29udGVudHMgNCAwIFIKICA+PgplbmRvYmoKCjQgMCBvYmoKICA8PCAvTGVuZ3RoIDU1ID4+CnN0cmVhbQogIEJUCiAgICAvRjEgMTggVGYKICAgIDE4MCA3MDAgVGQKICAgIChFVklDRVJUSUEgLSBUZXN0IERvY3VtZW50KSBUagogIEVUCmVuZHN0cmVhbQplbmRvYmoKCnhyZWYKMCA1CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxOCAwMDAwMCBuIAowMDAwMDAwMDc3IDAwMDAwIG4gCjAwMDAwMDAxNzggMDAwMDAgbiAKMDAwMDAwMDQ1NyAwMDAwMCBuIAp0cmFpbGVyCiAgPDwgIC9Sb290IDEgMCBSCiAgICAgIC9TaXplIDUKICA+PgpzdGFydHhyZWYKNTY1CiUlRU9G",
                        "attributes": [
                            {
                                "Key": "RequireContentCommitment", "Value": True
                            },
                            { "Key": "RequireContentCommitmentOrder", "Value": 1
                            }
                        ]
                    },
                    {
                        "Filename": "attach2.pdf",
                        "MimeType": "application/pdf",
                        "Data": "JVBERi0xLjEKJcKlwrHDqwoKMSAwIG9iagogIDw8IC9UeXBlIC9DYXRhbG9nCiAgICAgL1BhZ2VzIDIgMCBSCiAgPj4KZW5kb2JqCgoyIDAgb2JqCiAgPDwgL1R5cGUgL1BhZ2VzCiAgICAgL0tpZHMgWzMgMCBSXQogICAgIC9Db3VudCAxCiAgICAgL01lZGlhQm94IFswIDAgNTk1IDgyMl0KICA+PgplbmRvYmoKCjMgMCBvYmoKICA8PCAgL1R5cGUgL1BhZ2UKICAgICAgL1BhcmVudCAyIDAgUgogICAgICAvUmVzb3VyY2VzCiAgICAgICA8PCAvRm9udAogICAgICAgICAgIDw8IC9GMQogICAgICAgICAgICAgICA8PCAvVHlwZSAvRm9udAogICAgICAgICAgICAgICAgICAvU3VidHlwZSAvVHlwZTEKICAgICAgICAgICAgICAgICAgL0Jhc2VGb250IC9UaW1lcy1Sb21hbgogICAgICAgICAgICAgICA+PgogICAgICAgICAgID4+CiAgICAgICA+PgogICAgICAvQ29udGVudHMgNCAwIFIKICA+PgplbmRvYmoKCjQgMCBvYmoKICA8PCAvTGVuZ3RoIDU1ID4+CnN0cmVhbQogIEJUCiAgICAvRjEgMTggVGYKICAgIDE4MCA3MDAgVGQKICAgIChFVklDRVJUSUEgLSBUZXN0IERvY3VtZW50KSBUagogIEVUCmVuZHN0cmVhbQplbmRvYmoKCnhyZWYKMCA1CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAxOCAwMDAwMCBuIAowMDAwMDAwMDc3IDAwMDAwIG4gCjAwMDAwMDAxNzggMDAwMDAgbiAKMDAwMDAwMDQ1NyAwMDAwMCBuIAp0cmFpbGVyCiAgPDwgIC9Sb290IDEgMCBSCiAgICAgIC9TaXplIDUKICA+PgpzdGFydHhyZWYKNTY1CiUlRU9G",
                        "attributes": [
                            {
                                "Key": "RequireContentCommitment", "Value": True
                            },
                            {
                                "Key": "RequireContentCommitmentOrder", "Value": 2
                            }
                        ]
                    }
                ],
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

                print(response.text)
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
            # elif action == 'rechazar':
            #     revision = Revision.objects.get(contrato_id=request.POST['id'])
            #     revision.estado = 'RC'
            #     revision.obs = request.POST['obs']
            #     revision.save()
            #     contrato = Contrato.objects.get(pk=request.POST['id'])
            #     url = contrato.archivo
            #     os.remove(str(url))
            #     contrato.archivo = None
            #     contrato.estado_contrato = 'RC'
            #     contrato.save()
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
