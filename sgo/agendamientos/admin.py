from django.contrib import admin
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
#Models

# Agendamientos
from agendamientos.models import CentroMedico, Agendamiento
# Clientes
from clientes.models import Planta
#User
from users.models import User, Trabajador


class AgendamientoSetResource(resources.ModelResource):
    trabajador = fields.Field(column_name='trabajador', attribute='trabajador', widget=ForeignKeyWidget(Trabajador, 'nombre'))
    planta = fields.Field(column_name='planta', attribute='planta', widget=ForeignKeyWidget(Planta, 'nombre'))

    class Meta:
        model = Agendamiento
        fields = ('id', 'tipo', 'referido', 'hal2', 'fecha_ingreso_estimada', 'fecha_agenda_evaluacion', 'estado', 'status', )

