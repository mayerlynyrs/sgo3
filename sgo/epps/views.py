"""Epps views."""

# Django
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, ProtectedError
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView
# Create your views here.
# Models
from epps.models import TipoInsumo, Insumo, Convenio
from clientes.models import Planta
# From
from epps.forms import TipoInsumoForm, InsumoForm, ConvenioForm


class TipoListView(TemplateView):
    template_name = 'epps/tipo_insumo_list.html'

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
                for i in TipoInsumo.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                tipo = TipoInsumo()
                tipo.nombre = request.POST['nombre'].lower()
                tipo.status = True
                # espec.created_date = request.POST['created_date']
                tipo.save()
            elif action == 'edit':
                tipo = TipoInsumo.objects.get(pk=request.POST['id'])
                tipo.nombre = request.POST['nombre'].lower()
                tipo.save()
            elif action == 'delete':
                tipo = TipoInsumo.objects.get(pk=request.POST['id'])
                tipo.status = False
                tipo.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de Insumos'
        context['list_url'] = reverse_lazy('epps:tipo/list')
        context['entity'] = 'TipoInsumos'
        context['form'] = TipoInsumoForm()
        return context


class InsumoView(TemplateView):
    template_name = 'epps/insumo_list.html'

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
                for i in Insumo.objects.filter(status=True):
                    data.append(i.toJSON())
            elif action == 'add':
                insumo = Insumo()
                insumo.codigo_externo = request.POST['codigo_externo'].lower()
                insumo.nombre = request.POST['nombre'].lower()
                insumo.costo = request.POST['costo']
                insumo.tipo_insumo_id = request.POST['tipo_insumo']
                insumo.status = True
                insumo.save()
            elif action == 'edit':
                insumo = Insumo.objects.get(pk=request.POST['id'])
                insumo.codigo_externo = request.POST['codigo_externo'].lower()
                insumo.nombre = request.POST['nombre'].lower()
                insumo.costo = request.POST['costo']
                insumo.tipo_insumo_id = request.POST['tipo_insumo']
                insumo.save()
            elif action == 'delete':
                insumo = Insumo.objects.get(pk=request.POST['id'])
                insumo.status = False
                insumo.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Insumos'
        context['list_url'] = reverse_lazy('epps:insumo')
        context['entity'] = 'Insumos'
        context['form'] = InsumoForm()
        return context