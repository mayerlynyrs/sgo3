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
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.views.generic import TemplateView
# Model
from clientes.models import Planta
from examenes.models import Examen, Bateria
# Form
from examenes.forms import ExamenForm, BateriaForm

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
                exam.nombre = request.POST['nombre']
                exam.valor = request.POST['valor']
                exam.status = True
                # espec.created_date = request.POST['created_date']
                exam.save()
            elif action == 'edit':
                exam = Examen.objects.get(pk=request.POST['id'])
                exam.nombre = request.POST['nombre']
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
                    nombre = request.POST['nombre'],
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
                print(examenes)
                print("----")
                print(examen)
                exam.nombre = request.POST['nombre']
                # exam.examen = request.POST['examen']
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
