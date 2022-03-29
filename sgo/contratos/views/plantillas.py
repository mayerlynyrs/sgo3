"""Plantillas views."""

# Django
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, ProtectedError
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView
# Models
from contratos.models import Plantilla
from clientes.models import Planta
# From
from contratos.forms import CrearPlantillaForm, ActualizarPlantillaForm


class PlantillaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Plantilla List
    Vista para listar todos las plantilla según el usuario y sus las plantas
    relacionadas.
    """
    model = Plantilla
    template_name = "contratos/plantilla_list.html"
    paginate_by = 25
    ordering = ['plantas', 'nombre', ]

    permission_required = 'contratos.view_plantilla'
    raise_exception = True

    def get_queryset(self):
        search = self.request.GET.get('q')
        planta = self.kwargs.get('planta_id', None)

        if planta == '':
            planta = None

        if search:
            # Si el usuario no se administrador se despliegan las plantillas en estado activo
            # de las plantas a las que pertenece el usuario, según el critero de busqueda.
            if not self.request.user.groups.filter(name__in=['Administrador', ]).exists():
                queryset = super(PlantillaListView, self).get_queryset().filter(
                    Q(activo=True),
                    Q(plantas__in=self.request.user.planta.all()),
                    Q(nombre__icontains=search)
                ).distinct()
            else:
                # Si el usuario es administrador se despliegan todos las plantillas
                # segun el critero de busqueda.
                queryset = super(PlantillaListView, self).get_queryset().filter(
                    Q(nombre__icontains=search)
                ).distinct()
        else:
            # Si el usuario no es administrador, se despliegan las plantillas en estado
            # activo de las plantas a las que pertenece el usuario.
            if not self.request.user.groups.filter(name__in=['Administrador']).exists():
                queryset = super(PlantillaListView, self).get_queryset().filter(
                    Q(activo=True),
                    Q(plantas__in=self.request.user.planta.all())
                ).distinct()
            else:
                # Si el usuario es administrador, se despliegan todos las plantillas.
                if planta is None:
                    queryset = super(PlantillaListView, self).get_queryset()
                else:
                    # Si recibe la planta, solo muestra las plantillas que pertenecen a esa planta.
                    queryset = super(PlantillaListView, self).get_queryset().filter(
                        Q(plantas=planta)
                    ).distinct()

        return queryset


@login_required
@permission_required('contratos.change_plantilla', raise_exception=True)
def update_plantilla(request, plantilla_id):

    plantilla = get_object_or_404(Plantilla, pk=plantilla_id)

    # Se obtienen las plantas del usuario.
    try:
        plantas_usuario = Planta.objects.values_list('id', flat=True).filter(user=request.user)
    except:
        plantas_usuario = ''

    if request.method == 'POST':

        form = ActualizarPlantillaForm(data=request.POST, instance=plantilla, files=request.FILES, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Plantilla actualizada exitosamente')
            page = request.GET.get('page')
            if page != '':
                response = redirect('contratos:list-plantilla')
                response['Location'] += '?page=' + page
                return response
            else:
                return redirect('contratos:list-plantilla')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = ActualizarPlantillaForm(instance=plantilla,
                                       initial={'plantas': list(plantas_usuario), },
                                       user=request.user)

    return render(
        request=request,
        template_name='contratos/plantilla_create.html',
        context={
            'plantilla': plantilla,
            'form': form
        })

@login_required
@permission_required('contratos.add_plantilla', raise_exception=True)
def create_plantilla(request):
    if request.method == 'POST':

        form = CrearPlantillaForm(data=request.POST, files=request.FILES, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Plantilla Creada Exitosamente')

            return redirect('contratos:list-plantilla')
        else:
            messages.error(request, 'Por favor revise el formulario e intentelo de nuevo.')
    else:
        form = CrearPlantillaForm(user=request.user)

    return render(request, 'contratos/plantilla_create.html', {
        'form': form,
    })


@login_required
def delete_plantilla(request, object_id, template_name='contratos/plantilla_delete.html'):
    data = dict()
    object = get_object_or_404(Plantilla, pk=object_id)
    if request.method == 'POST':
        try:
            object.delete()
            messages.success(request, 'Plantilla eliminada exitosamente')
        except ProtectedError:
            messages.error(request, 'La plantilla no se pudo eliminar.')
            return redirect('contratos:update-plantilla', object_id)

        return redirect('contratos:list-plantilla')

    context = {'object': object}
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request
    )
    return JsonResponse(data)
