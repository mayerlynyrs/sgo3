"""Examénes Template Tags."""

import os
from django import template
from examenes.models import Evaluacion, Requerimiento as RequerimientoExam
register = template.Library()


@register.filter("estado_req_exam")
def estado_req_exam(value):

    estado = {
        RequerimientoExam.APROBADO: '<span class="label label-warning"><i class="fa fa-chain margin-r-5"></i>APROBADO</span>',
        RequerimientoExam.RECHAZADO: '<span class="label label-green">RECHAZADO</span>',
        RequerimientoExam.ENVIADO: '<span class="label label-danger">ENVIADO</span>',
    }

    return estado
    # return estado[value]

@register.filter('nombre_doc')
def nombre_doc(value):
    return value[0:-4]


# @register.filter("estado")
# def estado(value):

#     estado_evalu_exam = {
#         Evaluacion.RECOMENDABLE: '<span class="label label-warning"><i class="fa fa-chain margin-r-5"></i>RECOMENDABLE</span>',
#         Evaluacion.NO_RECOMENDABLE: '<span class="label label-green">NO RECOMENDABLE</span>',
#     }

#     return estado_evalu_exam


@register.filter("tag_estado_evaluacion")
def tag_estado_evaluacion(value):

    if value is 'R':
        estado = '<i class="fas fa-check text-success"></i> RECOMENDABLE'
    else:
        estado = '<i class="fas fa-ban text-danger"></i> NO RECOMENDABLE'

    return estado
