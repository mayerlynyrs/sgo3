from asyncio.windows_events import NULL
from django.shortcuts import render

# Create your views here.
"""Examenes  Views."""

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, ProtectedError
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.views.generic import TemplateView
# Model
from clientes.models import Planta
from examenes.models import Examen, Bateria, CentroMedico, Evaluacion, Requerimiento as RequerimientoExam
from agendamientos.models import Agendamiento
from users.models import Trabajador
# Form
from examenes.forms import ExamenForm, BateriaForm, AgendaGeneralForm, CentroForm, EvaluacionGeneralForm, ReportForm, RevExamenForm, EvaluacionMassoForm, AgendaMassoForm
from psicologos.forms import RevisionForm

class ExamenView(TemplateView):
    template_name = 'examenes/examen_list.html'

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
                for i in Examen.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                exam = Examen()
                exam.nombre = request.POST['nombre'].lower()
                exam.valor = request.POST['valor']
                exam.status = True
                # espec.created_date = request.POST['created_date']
                exam.save()
            elif action == 'edit':
                exam = Examen.objects.get(pk=request.POST['id'])
                exam.nombre = request.POST['nombre'].lower()
                exam.valor = request.POST['valor']
                exam.save()
            elif action == 'delete':
                exam = Examen.objects.get(pk=request.POST['id'])
                exam.status = False
                exam.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Exámenes'
        context['list_url'] = reverse_lazy('examenes:examen')
        context['entity'] = 'Examenes'
        context['form'] = ExamenForm()
        return context

class BateriaView(TemplateView):
    template_name = 'examenes/bateria_list.html'

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
                for i in Bateria.objects.filter(status=True):
                    data.append(i.toJSON())
                #     print("-------")
                # print(data)
            elif action == 'add':
                examen = request.POST.getlist('examen')
                exam = Bateria.objects.create(
                    nombre = request.POST['nombre'].lower(),
                    status = True,
                    )

                for i in examen:
                    exam.examen.add(i)
                # exam.save()
            elif action == 'edit':
                examen = request.POST.getlist('examen')
                pk=request.POST['id']
                examenes = request.POST.getlist('examen', pk)
                exam = Bateria.objects.get(pk=request.POST['id'])
                ex = []
                for d in exam.examen.all():
                    ex.append(d.id )
                for i in ex:
                    exam.examen.remove(i)
                exam.nombre = request.POST['nombre'].lower()
                for i in examen:
                    exam.examen.add(i)
                exam.save()
            elif action == 'delete':
                exam = Bateria.objects.get(pk=request.POST['id'])
                exam.status = False
                exam.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Batería'
        context['list_url'] = reverse_lazy('examenes:bateria')
        context['entity'] = 'Bateria'
        context['form'] = BateriaForm()
        return context


class AgendaList(TemplateView):
    template_name = 'examenes/tabla_agenda.html'

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
                for i in Agendamiento.objects.filter(Q(estado='E') & Q(tipo_evaluacion='GEN')& Q(status=True)):
                    data.append(i.toJSON())
            elif action == 'edit':
                agenda = Agendamiento.objects.get(pk=request.POST['id'])
                if "referido" in request.POST:
                    estado = True
                    agenda.referido =  estado
                else:
                    estado = False
                    agenda.referido =  estado
                agenda.estado = request.POST['estado']
                agenda.tipo = request.POST['tipo']
                agenda.fecha_ingreso_estimada = request.POST['fecha_ingreso_estimada']
                agenda.fecha_agenda_evaluacion = request.POST['fecha_agenda_evaluacion']
                agenda.planta_id = request.POST['planta']
                agenda.cargo_id = request.POST['cargo']
                agenda.centro_id = request.POST['centromedico']
                agenda.bateria_id = request.POST['bateria']
                agenda.obs = request.POST['obs']
                agenda.save()
            elif action == 'delete':
                agenda = Agendamiento.objects.get(pk=request.POST['id'])
                agenda.status = False
                agenda.save()
            elif action == 'evaluacion_add':
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
                evaluacion.valor = request.POST['valor']
                evaluacion.fecha_termino = request.POST['fecha_termino']
                evaluacion.tipo_evaluacion = "GEN"
                evaluacion.trabajador_id = request.POST['user_id']
                evaluacion.centro_id = request.POST['centromedico']
                evaluacion.bateria_id = request.POST['bateria']
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
        context['title'] = 'Listado de Evaluaciones'
        context['list_url'] = reverse_lazy('examenes:listAgenda')
        context['entity'] = 'Examenes'
        context['form'] = AgendaGeneralForm()
        context['form1'] = EvaluacionGeneralForm()
        return context


class AgendaListMasso(TemplateView):
    template_name = 'examenes/tabla_agenda_masso.html'

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
                for i in Agendamiento.objects.filter(Q(estado='E') & Q(tipo_evaluacion='MAS')& Q(status=True)):
                    data.append(i.toJSON())
            elif action == 'edit':
                agenda = Agendamiento.objects.get(pk=request.POST['id'])
                if "referido" in request.POST:
                    estado = True
                    agenda.referido =  estado
                else:
                    estado = False
                    agenda.referido =  estado
                agenda.estado = request.POST['estado']
                agenda.tipo = request.POST['tipo']
                agenda.fecha_ingreso_estimada = request.POST['fecha_ingreso_estimada']
                agenda.fecha_agenda_evaluacion = request.POST['fecha_agenda_evaluacion']
                agenda.planta_id = request.POST['planta']
                agenda.cargo_id = request.POST['cargo']
                agenda.obs = request.POST['obs']
                agenda.save()
            elif action == 'delete':
                agenda = Agendamiento.objects.get(pk=request.POST['id'])
                agenda.status = False
                agenda.save()
            elif action == 'evaluacion_add':
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
                evaluacion.valor = request.POST['valor']
                evaluacion.fecha_termino = request.POST['fecha_termino']
                evaluacion.tipo_evaluacion = "MAS"
                evaluacion.trabajador_id = request.POST['user_id']
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
        context['title'] = 'Listado de Evaluaciones'
        context['list_url'] = reverse_lazy('examenes:listAgenda')
        context['entity'] = 'Examenes'
        context['form'] = AgendaMassoForm()
        context['form1'] = EvaluacionMassoForm()
        return context


class CentroMedicoView(TemplateView):
    template_name = 'examenes/centromedico_list.html'

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
                for i in CentroMedico.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                centro = CentroMedico()
                centro.nombre = request.POST['nombre'].lower()
                centro.direccion = request.POST['direccion'].lower()
                centro.region_id = request.POST['region']
                centro.provincia_id = request.POST['provincia']
                centro.ciudad_id = request.POST['ciudad']
                centro.status = True
                centro.save()
            elif action == 'edit':
                centro = CentroMedico.objects.get(pk=request.POST['id'])
                centro.nombre = request.POST['nombre'].lower()
                centro.direccion = request.POST['direccion'].lower()
                centro.region_id = request.POST['region']
                centro.provincia_id = request.POST['provincia']
                centro.ciudad_id = request.POST['ciudad']
                centro.status = True
                centro.save()
            elif action == 'delete':
                centro = CentroMedico.objects.get(pk=request.POST['id'])
                centro.status = False
                centro.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Centro Médico'
        context['list_url'] = reverse_lazy('examenes:bateria')
        context['entity'] = 'Centro Médico'
        context['form'] = CentroForm()
        return context


class EvalTerminadasView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Psicologo List
    Vista para listar todos los psicologo según el usuario y sus las plantas
    relacionadas.
    """

    model = Evaluacion
    template_name = 'examenes/evaluacionesTerminadas.html'
    permission_required = 'examenes.view_evaluacion'
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
                   for i in search.filter(Q(fecha_inicio__range=[start_date, end_date]) & Q(tipo_evaluacion = 'GEN')):
                        data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte Evaluaciones'
        context['list_url'] = reverse_lazy('psicologos:evalu_terminadas')
        context['entity'] = 'Salud'
        context['form'] = ReportForm()
        return context


class EvalTerminadasMassoView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Psicologo List
    Vista para listar todos los psicologo según el usuario y sus las plantas
    relacionadas.
    """

    model = Evaluacion
    template_name = 'examenes/evaluacionesTerminadasMasso.html'
    permission_required = 'examenes.view_evaluacion'
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
                   for i in search.filter(Q(fecha_inicio__range=[start_date, end_date]) & Q(tipo_evaluacion = 'MAS')):
                        data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte Evaluaciones'
        context['list_url'] = reverse_lazy('psicologos:evalu_terminadas')
        context['entity'] = 'Salud'
        context['form'] = ReportForm()
        return context


class ExaSolicitudesList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Psicólogos Pendientes Solicitudes List
    Vista para listar todas las solicitudes pendientes de los psicologos
    .
    """
    model = RequerimientoExam
    # RequerimientoExam.objects.filter(Q(estado='E') & Q(psicologico=True) & Q(status=True)):
    template_name = "examenes/solicitudes_list.html"

    permission_required = 'psicologos.view_psicologico'
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
                queryset = super(ExaSolicitudesList, self).get_queryset().filter(
                    Q(estado='E'),
                    Q(bateria_id__isnull=False),
                    Q(status=True),
                    Q(planta__in=self.request.user.planta.all()),
                    Q(nombre__icontains=search)
                ).distinct()
            else:
                # Si el usuario es administrador se despliegan todos los requerimientos
                # segun el critero de busqueda.
                queryset = super(ExaSolicitudesList, self).get_queryset().filter(
                    Q(estado='E'),
                    Q(status=True),
                    Q(bateria_id__isnull=False),
                    Q(nombre__icontains=search)
                ).distinct()
        else:
            # Si el usuario no es administrador, se despliegan los requerimientos en estado
            # status de las plantas a las que pertenece el usuario.
            if not self.request.user.groups.filter(name__in=['Administrador']).exists():
                queryset = super(ExaSolicitudesList, self).get_queryset().filter(
                    Q(estado='E'),
                    Q(bateria_id__isnull=False),
                    Q(status=True),
                    Q(planta__in=self.request.user.planta.all())
                ).distinct()
            else:
                # Si el usuario es administrador, se despliegan todos los requerimientos.
                if planta is None:
                    queryset = super(ExaSolicitudesList, self).get_queryset().filter(
                        Q(estado='E'),
                        Q(status=True),
                        Q(bateria_id__isnull=False),
                    ).distinct()
                else:
                    # Si recibe la planta, solo muestra los requerimientos que pertenecen a esa planta.
                    queryset = super(ExaSolicitudesList, self).get_queryset().filter(
                        Q(estado='E'),
                        Q(status=True),
                        Q(bateria_id__isnull=False),
                        Q(planta=planta)
                    ).distinct()
        print(queryset)
        return queryset
class ExaSolicitudesListMasso(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Psicólogos Pendientes Solicitudes List
    Vista para listar todas las solicitudes pendientes de los psicologos
    .
    """
    model = RequerimientoExam
    # RequerimientoExam.objects.filter(Q(estado='E') & Q(psicologico=True) & Q(status=True)):
    template_name = "examenes/solicitudes_list_masso.html"

    permission_required = 'psicologos.view_psicologico'
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
                queryset = super(ExaSolicitudesListMasso, self).get_queryset().filter(
                    Q(estado='E'),
                    Q(masso=True),
                    Q(status=True),
                    Q(planta__in=self.request.user.planta.all()),
                    Q(nombre__icontains=search)
                ).distinct()
            else:
                # Si el usuario es administrador se despliegan todos los requerimientos
                # segun el critero de busqueda.
                queryset = super(ExaSolicitudesListMasso, self).get_queryset().filter(
                    Q(estado='E'),
                    Q(status=True),
                    Q(masso=True),
                    Q(nombre__icontains=search)
                ).distinct()
        else:
            # Si el usuario no es administrador, se despliegan los requerimientos en estado
            # status de las plantas a las que pertenece el usuario.
            if not self.request.user.groups.filter(name__in=['Administrador']).exists():
                queryset = super(ExaSolicitudesListMasso, self).get_queryset().filter(
                    Q(estado='E'),
                    Q(masso=True),
                    Q(status=True),
                    Q(planta__in=self.request.user.planta.all())
                ).distinct()
            else:
                # Si el usuario es administrador, se despliegan todos los requerimientos.
                if planta is None:
                    queryset = super(ExaSolicitudesListMasso, self).get_queryset().filter(
                        Q(estado='E'),
                        Q(status=True),
                        Q(masso=True),
                    ).distinct()
                else:
                    # Si recibe la planta, solo muestra los requerimientos que pertenecen a esa planta.
                    queryset = super(ExaSolicitudesListMasso, self).get_queryset().filter(
                        Q(estado='E'),
                        Q(status=True),
                        Q(masso=True),
                        Q(planta=planta)
                    ).distinct()
        print(queryset)
        return queryset



@login_required
@permission_required('examenes.view_examen', raise_exception=True)
def detail_solicitud(request, trabajador_id, template_name='examenes/solicitudes_detail.html'):
    data = dict()
    evaluacion = Evaluacion.objects.filter(trabajador=trabajador_id)
    # evaluacion = get_object_or_404(Evaluacion, trabajador=trabajador_id)
    evalua = Evaluacion.objects.filter(trabajador=trabajador_id, tipo_evaluacion ="PSI")
    trabajador = Evaluacion.objects.values_list('trabajador', flat=True).filter(trabajador=trabajador_id,tipo_evaluacion ="PSI")
    print('examenes',evalua )

    context={
        'evaluacion': evaluacion,
        'evalua': Evaluacion.objects.filter(trabajador=trabajador_id, tipo_evaluacion ="GEN"),
        'trabajador': Trabajador.objects.get(id=trabajador_id),
    }
    
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )

    return JsonResponse(data)

@login_required
@permission_required('examenes.view_examen', raise_exception=True)
def detail_solicitud_masso(request, trabajador_id, template_name='examenes/solicitudes_detail_masso.html'):
    data = dict()
    evaluacion = Evaluacion.objects.filter(trabajador=trabajador_id)
    # evaluacion = get_object_or_404(Evaluacion, trabajador=trabajador_id)
    evalua = Evaluacion.objects.filter(trabajador=trabajador_id, tipo_evaluacion ="PSI")
    trabajador = Evaluacion.objects.values_list('trabajador', flat=True).filter(trabajador=trabajador_id,tipo_evaluacion ="MAS")
    print('examenes',evalua )

    context={
        'evaluacion': evaluacion,
        'evalua': Evaluacion.objects.filter(trabajador=trabajador_id, tipo_evaluacion ="MAS"),
        'trabajador': Trabajador.objects.get(id=trabajador_id),
    }
    
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )

    return JsonResponse(data)

def revision_solicitudes(request, requerimiento_id, template_name='examenes/revision_estado.html'):
    data = dict()
    requerimiento = get_object_or_404(RequerimientoExam, pk=requerimiento_id)

    if request.method == 'POST':

        form = RevisionForm(request.POST or None, instance=requerimiento)

        if form.is_valid():
            requerimiento = form.save()
            messages.success(request, 'Solicitud actualizada Exitosamente')
            page = request.GET.get('page')
            if page != '':
                response = redirect('examenes:list-solicitudes')
                # response['Location'] += '?page=' + str(page)
                return response
            else:
                return redirect('examenes:list-solicitudes')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = RevisionForm(instance=requerimiento,)

    context={
        'requerimiento': requerimiento,
        'form': RevisionForm
    }
    
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)