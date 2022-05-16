from asyncio.windows_events import NULL
from django.shortcuts import render
from django.views.generic import ListView
from requerimientos.models import *
from consultas.forms import ConsultaClienteForm
from sgo import requerimientos
from consultas.forms import ConsultaClienteForm
from clientes.models import Negocio, Planta
from django.db import connection



# Create your views here.
# Planta
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
        else:
            data = Cliente.objects.raw("SELECT * FROM vista_consulta_requerimiento WHERE id = %s", [planta])
            context = {'data': data}
            context ['form'] = ConsultaClienteForm(instance=Cliente)
            return render(request, 'consultas/consulta_requerimiento.html', context)

