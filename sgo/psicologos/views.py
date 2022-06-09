from telnetlib import STATUS
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, ProtectedError
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from datetime import datetime , timedelta
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from psicologos.forms import UserAgendar, AgendaPsicologos, ReportForm, EvaluacionPsicologica
# Model
from psicologos.models import Psicologico, Agenda
from agendamientos.models import Agendamiento
from users.models import User, Trabajador
from examenes.models import Evaluacion
# Create your views here.


class PsicologosCalendarioView(ListView):
    """Psicologos Calendario List
    Vista para listar todos los psicologo según el usuario y sus las plantas
    relacionadas.
    """
    template_name = 'psicologos/agendar.html'
    model = Agenda

    def get_queryset(self):
        queryset = Agenda.objects.filter(status = True)
        return queryset
        

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['form'] = UserAgendar()
  
        return context


class AgendaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            agenda_form = UserAgendar(data=request.POST)
            if agenda_form.is_valid():
                agenda = agenda_form.save(commit=False)
                agenda.status = True
                # agenda.fecha_agenda_evaluacion = Null
                agenda.save()
                agenda = agenda_form.save()
                messages.success(request, 'Agenda Creado Exitosamente')
                return redirect('psicologos:listAgenda')
            else:
                messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
        else:
            agenda_form = UserAgendar(user=request.user)
        return render(request, 'psicologos/agendar.html', {
            'form': agenda_form,
        })

    permission_required = 'psicologos.add_agenda'
    raise_exception = True


class AgendaList(TemplateView):
    template_name = 'psicologos/tabla_agenda.html'

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
                for i in Agendamiento.objects.filter(Q(estado='E') & Q(tipo_evaluacion='PSI')):
                    data.append(i.toJSON())
            elif action == 'edit':
                agenda = Agendamiento.objects.get(pk=request.POST['id'])
                if "referido" in request.POST:
                    estado = True
                    agenda.referido =  estado
                else:
                    estado = False
                    agenda.referido =  estado
                if "Hal2" in request.POST:
                    estado = True
                    agenda.Hal2 =  estado
                else:
                    estado = False
                    agenda.Hal2 =  estado  
                agenda.estado = request.POST['estado']
                agenda.tipo = request.POST['tipo']
                agenda.fecha_ingreso_estimada = request.POST['fecha_ingreso_estimada']
                agenda.fecha_agenda_evaluacion = request.POST['fecha_agenda_evaluacion']
                agenda.planta_id = request.POST['planta']
                agenda.cargo_id = request.POST['cargo']
                agenda.psico_id = request.POST['psico']
                agenda.obs = request.POST['obs']
                agenda.save()
            elif action == 'delete':
                agenda = Agendamiento.objects.get(pk=request.POST['id'])
                agenda.status = False
                agenda.save()
            elif action == 'evaluacion_add':
                fechainicio = request.POST['fecha_inicio']
                f = fechainicio.split("-")
                anio = int(f[0]) + 2 
                fechafinal = str(anio) + "-" + str(f[1]) + "-" + str(f[2])
                fechafinal2 = datetime.strptime(fechafinal, '%Y-%m-%d')
                if "referido" in request.POST:
                    estado = True
                else:
                    estado = False
                evaluacion = Evaluacion()
                evaluacion.estado = request.POST['estado']
                evaluacion.referido =  estado
                evaluacion.fecha_inicio = request.POST['fecha_inicio']
                evaluacion.tipo = request.POST['tipo']
                evaluacion.resultado = request.POST['resultado']
                evaluacion.valor = 0
                evaluacion.fecha_termino = fechafinal2
                evaluacion.tipo_evaluacion = "PSI"
                evaluacion.trabajador_id = request.POST['user_id']
                evaluacion.psicologo_id = request.POST['psicologo']
                evaluacion.planta_id = request.POST['planta']
                evaluacion.cargo_id = request.POST['cargo']
                evaluacion.archivo = request.FILES['archivo']
                if "archivo2" in request.FILES:
                    evaluacion.archivo2 = request.FILES['archivo2']
                evaluacion.save()
                agenda = Agendamiento.objects.get(pk=request.POST['id'])
                agenda.estado = 'A'
                agenda.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        psicologos  = User.objects.filter(groups__name='Psicologo')
        # print ('psicologos', psicologos)
        context['title'] = 'Listado de Evaluaciones'
        context['list_url'] = reverse_lazy('psicologos:listAgenda')
        context['entity'] = 'Salud'
        context['form'] = AgendaPsicologos(users_evaluador=psicologos)
        context['form1'] = EvaluacionPsicologica()
        return context


class EvalTerminadasView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Psicologo List
    Vista para listar todos los psicologo según el usuario y sus las plantas
    relacionadas.
    """

    model = Evaluacion
    template_name = 'psicologos/evaluacionesTerminadas.html'
    permission_required = 'psicologos.view_evaluacionpsicologico'
    raise_exception = True

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Evaluacion.objects.all()
                if len(start_date) and len(end_date):
                   for i in search.filter(Q(fecha_inicio__range=[start_date, end_date]) & Q(tipo_evaluacion = 'PSI')):
                        data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte Evaluaciones'
        context['list_url'] = reverse_lazy('psicologos:evaTerminadas')
        context['entity'] = 'Salud'
        context['form'] = ReportForm()
        return context
