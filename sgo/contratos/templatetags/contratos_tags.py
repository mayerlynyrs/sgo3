"""Contratos Template Tags."""

import os
from django import template
from contratos.models import Contrato
register = template.Library()


@register.filter("estado_firma")
def estado_firma(value):

    estado = {
        Contrato.POR_FIRMAR: '<span class="label label-warning"><i class="fa fa-chain margin-r-5"></i>POR FIRMAR</span>',
        Contrato.FIRMADO_TRABAJADOR: '<span class="label label-success"><i class="fa fa-lock margin-r-5"></i> FIRMADO TRABAJADOR</span>',
        Contrato.FIRMADO_EMPLEADOR: '<span class="label label-purple">FIRMADO EMPLEADOR</span>',
        Contrato.FIRMADO: '<span class="label label-green">FIRMADO</span>',
        Contrato.OBJETADO: '<span class="label label-danger">OBJETADO</span>',
    }

    # return estado
    return estado[value]


@register.filter("estado_contrato")
def estado_contrato(value):

    estado = {
        Contrato.CREADO: '<span class="label label-warning"><i class="fa fa-chain margin-r-5"></i>CREADO</span>',
        Contrato.PROCESO_VALIDACION: '<span class="label label-success"><i class="fa fa-lock margin-r-5"></i>PROCESO VALIDACIÓN</span>',
        Contrato.PENDIENTE_BAJA: '<span class="label label-purple">PENDIENTE BAJA</span>',
        Contrato.BAJADO: '<span class="label label-purple">BAJADO</span>',
        Contrato.APROBADO: '<span class="label label-green">APROBADO</span>',
        Contrato.RECHAZADO: '<span class="label label-danger">RECHAZADO</span>',
    }

    return estado[value]

@register.filter('nombre_doc')
def nombre_doc(value):
    return value[0:-4]