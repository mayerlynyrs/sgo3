"""Contratos Template Tags."""

import os
from django import template
from contratos.models import Contrato
register = template.Library()


@register.filter("estado_firma")
def estado_firma(value):

    estado = {
        Contrato.POR_FIRMAR: '<span class="label label-warning">POR FIRMAR</span>',
        Contrato.ENVIADO_FIRMAR: '<span class="label label-info">ENVIADO FIRMAR</span>',
        Contrato.FIRMADO_TRABAJADOR: '<span class="label label-success">FIRMADO TRABAJADOR</span>',
        Contrato.FIRMADO_EMPLEADOR: '<span class="label label-purple">FIRMADO EMPLEADOR</span>',
        Contrato.FIRMADO: '<span class="label label-green">FIRMADO</span>',
        Contrato.OBJETADO: '<span class="label label-danger">OBJETADO</span>',
        Contrato.EXPIRADO: '<span class="label label-dark">EXPIRADO</span>',
    }

    # return estado
    return estado[value]


@register.filter("estado_contrato")
def estado_contrato(value):

    estado = {
        Contrato.CREADO: '<span class="label label-warning">CREADO</span>',
        Contrato.PROCESO_VALIDACION: '<span class="label label-success">PROCESO<br>VALIDACIÓN</span>',
        Contrato.PENDIENTE_BAJA: '<span class="label label-purple">PENDIENTE<br>BAJA</span>',
        Contrato.BAJADO: '<span class="label label-purple">BAJADO</span>',
        Contrato.APROBADO: '<span class="label label-green">APROBADO</span>',
        Contrato.RECHAZADO: '<span class="label label-danger">RECHAZADO</span>',
    }

    return estado[value]


@register.filter("estado_anexo")
def estado_anexo(value):

    estado = {
        Contrato.CREADO: '<span class="label label-warning">CREADO</span>',
        Contrato.PROCESO_VALIDACION: '<span class="label label-success">PROCESO<br>VALIDACIÓN</span>',
        Contrato.PENDIENTE_BAJA: '<span class="label label-purple">PENDIENTE<br>BAJA</span>',
        Contrato.BAJADO: '<span class="label label-purple">BAJADO</span>',
        Contrato.APROBADO: '<span class="label label-green">APROBADO</span>',
        Contrato.RECHAZADO: '<span class="label label-danger">RECHAZADO</span>',
    }

    return estado[value]

@register.filter('nombre_doc')
def nombre_doc(value):
    return value[0:-4]