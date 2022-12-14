from asyncio.windows_events import NULL
from telnetlib import STATUS
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, ProtectedError
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from datetime import datetime , timedelta
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
#enviar correo electronico 
from django.contrib import messages
from django.core.mail import send_mail


from agendamientos.forms import UserAgendar, UserAgendarSolicitud
# Model
from agendamientos.models import Agendamiento


# Create your views here.

class AgendaCalendarioView(ListView):
    """agenda general Calendario List
    Vista para listar todos los psicologo según el usuario y sus las plantas
    relacionadas.
    """
    template_name = 'agendamientos/agendar.html'
    model = Agendamiento
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['psicologo'] = Agendamiento.objects.filter(Q(status = True) & Q(tipo_evaluacion='PSI'))
        context['general'] = Agendamiento.objects.filter(Q(status = True) & Q(tipo_evaluacion='GEN'))
        context['form'] = UserAgendar()
  
        return context


class AgendaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            agenda_form = UserAgendar(data=request.POST)
            if agenda_form.is_valid():
                    if "psico" in request.POST:
                        agendar = Agendamiento()
                        agendar.requerimiento_id = request.POST['requerimiento']
                        agendar.tipo = request.POST['tipo']
                        agendar.trabajador_id = request.POST['trabajador']
                        agendar.fecha_ingreso_estimada = request.POST['fecha_ingreso_estimada']
                        agendar.planta_id = request.POST['planta']
                        agendar.cargo_id = request.POST['cargo']
                        if "referido" in request.POST:
                            estado = True
                        else:
                            estado = False
                        agendar.referido =  estado
                        if "hal2" in request.POST:
                            hal2 = True
                        else:
                            hal2 = False
                        agendar.referido =  estado
                        agendar.hal2 =  hal2
                        agendar.obs = request.POST['obs']
                        agendar.tipo_evaluacion = "PSI"
                        agendar.status = True
                        agendar.save()
                        send_mail(
                            'Nueva Solicitud de Agenda Prueba sgo3 ',
                            'Estimado(a) se a realizado un nueva solicitud de agendamiento psicologico para el trabajador ' + str(agendar.trabajador) +' con fecha de ingreso: ' 
                            + agendar.fecha_ingreso_estimada  ,
                            'psicologos@empresasintegra.cl',
                            ['soporte@empresasintegra.cl'],
                            fail_silently=False,
                        )
                    if "general" in request.POST:
                        agendar = Agendamiento()
                        agendar.requerimiento_id = request.POST['requerimiento']
                        agendar.tipo = request.POST['tipo']
                        agendar.trabajador_id = request.POST['trabajador']
                        agendar.fecha_ingreso_estimada = request.POST['fecha_ingreso_estimada']
                        agendar.planta_id = request.POST['planta']
                        agendar.cargo_id = request.POST['cargo']
                        agendar.bateria_id = request.POST['bateria']
                        if "referido" in request.POST:
                            estado = True
                        else:
                            estado = False
                        agendar.referido =  estado
                        agendar.obs = request.POST['obs']
                        agendar.tipo_evaluacion = "GEN"
                        agendar.status = True
                        agendar.save()
                        send_mail(
                            'Nueva Solicitud de Agenda Prueba sgo3 ',
                            'Estimado(a) se a realizado un nueva solicitud de agendamiento Examen General para el trabajador ' + str(agendar.trabajador) +' con fecha de ingreso: ' 
                            + agendar.fecha_ingreso_estimada  ,
                            'jcruces@empresasintegra.cl',
                            ['soporte@empresasintegra.cl'],
                            fail_silently=False,
                        )
                        if "masso" in request.POST:
                            agendar = Agendamiento()
                            agendar.requerimiento_id = request.POST['requerimiento']
                            agendar.tipo = request.POST['tipo']
                            agendar.trabajador_id = request.POST['trabajador']
                            agendar.fecha_ingreso_estimada = request.POST['fecha_ingreso_estimada']
                            agendar.planta_id = request.POST['planta']
                            agendar.cargo_id = request.POST['cargo']
                            if "referido" in request.POST:
                                estado = True
                            else:
                                estado = False
                            agendar.referido =  estado
                            agendar.obs = request.POST['obs']
                            agendar.tipo_evaluacion = "MAS"
                            agendar.status = True
                            agendar.save()
                            send_mail(
                                'Nueva Solicitud de Agenda Prueba sgo3 ',
                                'Estimado(a) se a realizado un nueva solicitud de agendamiento MASSO para el trabajador ' + str(agendar.trabajador) +' con fecha de ingreso: ' 
                                + agendar.fecha_ingreso_estimada  ,
                                'jcruces@empresasintegra.cl',
                                ['soporte@empresasintegra.cl'],
                                fail_silently=False,
                            )
                    messages.success(request, 'Agenda Creado Exitosamente')
                    return redirect('agendamientos:listAgenda')
            else:
                messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
        else:
            agenda_form = UserAgendar(user=request.user)
        return render(request, 'agendamientos/agendar.html', {
            'form': agenda_form,
        })

    permission_required = 'agendamientos.add_agendamiento'
    raise_exception = True



class SolicitudesUserView(TemplateView):
    """Profesion List
    Vista para listar todos los profesion según el usuario y sus las negocios
    relacionadas.
    """
    template_name = 'agendamientos/solicitudes.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata5':
                data = []
                for i in Agendamiento.objects.filter(created_by_id=user_id, status=True, fecha_agenda_evaluacion__isnull = True ):
                    data.append(i.toJSON())
            elif action == 'edit':
                agenda = Agendamiento.objects.get(pk=request.POST['id'])
                agenda.fecha_ingreso_estimada = request.POST['fecha_ingreso_estimada']
                agenda.save()
            elif action == 'delete':
                agenda = Agendamiento.objects.get(pk=request.POST['id'])
                agenda.status = False
                agenda.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            print(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte Evaluaciones'
        context['form'] = UserAgendarSolicitud()
        return context