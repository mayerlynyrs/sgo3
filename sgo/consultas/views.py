from asyncio.windows_events import NULL
from itertools import chain
from django.shortcuts import render
from django.views.generic import ListView
from requerimientos.models import Requerimiento, AreaCargo
from epps.models import Insumo, ConvenioRequerimiento, ConvenioRequerTrabajador
from consultas.forms import ConsultaClienteForm, ConsultaEppRequForm, EppRequerimientoForm, ConvenioClienteForm
from clientes.models import Cliente, Negocio, Planta
from django.db import connection


# Cliente / Planta
def load_plantas(request):
    cliente_id = request.GET.get('cliente')    
    plantas = Planta.objects.filter(cliente_id=cliente_id).order_by('nombre')
    context = {'plantas': plantas}
    return render(request, 'consultas/planta.html', context)


class ConsultaRequerimientoView(ListView):
    #model = Requerimiento
    form_class = ConsultaClienteForm
    template_name = 'consultas/consulta_requerimiento.html'
    
    
    def get_queryset(self):
        return Cliente.objects.raw("SELECT * FROM vista_consulta_requerimiento")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['form'] = ConsultaClienteForm(instance=Cliente)
        return context

def buscar_requerimiento(request):
    if request.method == 'POST':
        todo =  request.POST.get('todos')
        cliente = request.POST.get('cliente')
        planta = request.POST.get('planta')
        if todo:
            data = Cliente.objects.raw("SELECT * FROM vista_consulta_requerimiento")
            context = {'data': data}
            context ['form'] = ConsultaClienteForm(instance=Cliente)
            return render(request, 'consultas/consulta_requerimiento.html', context)
        if planta:
            data = Cliente.objects.raw("SELECT * FROM vista_consulta_requerimiento WHERE id = %s AND cliente_id = %s", [planta,cliente])
            context = {'data': data}
            context ['form'] = ConsultaClienteForm(instance=Cliente)
            return render(request, 'consultas/consulta_requerimiento.html', context)
        else:
            data = Cliente.objects.raw("SELECT * FROM vista_consulta_requerimiento WHERE cliente_id = %s", [cliente])
            context = {'data': data}
            context ['form'] = ConsultaClienteForm(instance=Cliente)
            return render(request, 'consultas/consulta_requerimiento.html', context)


# Requerimiento / Área-Cargo
def load_areas_cargos(request):
    requerimiento_id = request.GET.get('requerimiento')    
    areas_cargos = AreaCargo.objects.filter(requerimiento_id=requerimiento_id).order_by('area','cargo')
    context = {'areas_cargos': areas_cargos}
    return render(request, 'consultas/area_cargo.html', context)


class ConsultaEppView(ListView):
    #model = Convenio
    form_class = ConsultaEppRequForm
    template_name = 'consultas/consulta_epps.html'
    
    
    def get_queryset(self):
        return ConvenioRequerimiento.objects.all()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['form'] = ConsultaEppRequForm(instance=ConvenioRequerimiento)
        return context

def buscar_requerimiento_ac(request):
    if request.method == 'POST':
        # x = 1
        # y = 1
        todo =  request.POST.get('todos')
        requerimiento = request.POST.get('requerimiento')
        area_cargo = request.POST.get('area_cargo')
        if todo:
            # data = Requerimiento.objects.raw('SELECT * FROM consulta_epps_req01(%s, %s)', [x, y])
            # data = ConvenioRequerimiento.objects.raw("SELECT * FROM consulta_epps_req01(1, 1)")
            data = ConvenioRequerimiento.objects.all()
            context = {'data': data}
            context ['form'] = ConsultaEppRequForm(instance=ConvenioRequerTrabajador)
            return render(request, 'consultas/consulta_epps.html', context)
        if area_cargo:
            data = ConvenioRequerimiento.objects.filter(requerimiento_id=requerimiento, area_cargo_id=area_cargo)
            context = {'data': data}
            context ['form'] = ConsultaEppRequForm(instance=ConvenioRequerimiento)
            return render(request, 'consultas/consulta_epps.html', context)
        else:
            data = ConvenioRequerimiento.objects.filter(requerimiento_id=requerimiento)
            context = {'data': data}
            context ['form'] = ConsultaEppRequForm(instance=ConvenioRequerimiento)
            return render(request, 'consultas/consulta_epps.html', context)


class RequerimientoEppView(ListView):
    form_class = EppRequerimientoForm
    template_name = 'consultas/consulta_epps_requerimiento.html'
    
    
    def get_queryset(self):
        return ConvenioRequerimiento.objects.all()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['form'] = EppRequerimientoForm(instance=ConvenioRequerimiento)
        return context

def buscar_epps_requerimiento(request):
    if request.method == 'POST':
        requerimiento = request.POST.get('requerimiento')
        if requerimiento:
            data = Requerimiento.objects.raw('SELECT * FROM public.consulta_epps_req02(%s)', [requerimiento])
            # data = ConvenioRequerTrabajador.objects.raw("SELECT * FROM public.consulta_epps_req02(1)")
            context = {'data': data}
            context ['form'] = ConsultaEppRequForm(instance=ConvenioRequerTrabajador)
            return render(request, 'consultas/consulta_epps_requerimiento.html', context)


# EPPs / Convenio Cliente
class ConvenioClienteView(ListView):
    form_class = ConvenioClienteForm
    template_name = 'consultas/consulta_convenio_cliente.html'
    
    
    def get_queryset(self):
        return Cliente.objects.all()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['form'] = ConvenioClienteForm(instance=Cliente)
        return context

def buscar_convenio_cliente(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        if cliente:
            data = Cliente.objects.raw('SELECT * FROM public.consulta_epps_req03(%s)', [cliente])
            context = {'data': data}
            context ['form'] = ConvenioClienteForm(instance=Cliente)
            return render(request, 'consultas/consulta_convenio_cliente.html', context)
