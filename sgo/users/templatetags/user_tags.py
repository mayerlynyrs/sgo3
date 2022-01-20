"""Users Template Tags."""

import os
from django import template
from django.templatetags.static import static
from users.models import User
register = template.Library()


""" @register.filter("sexo")
def sexo(value):
    if value == User.FEMALE:
        text = User.GENDER_CHOICES[0][1]
    else:
        text = User.GENDER_CHOICES[1][1]

    return text """

@register.filter("image_profile")
def image_profile(value):
    perfiles = {
        'Administrador': '<img src="{0}" alt="profile image" />'.format(static('img/admin_masculino.png')),
        'Administrador Contratos': '<img src="{0}" alt="profile image" />'.format(static('img/supervisor_masculino.png')),
        'Fiscalizador Interno': '<img src="{0}" alt="profile image" />'.format(static('img/fiscalizador_masculino.png')),
        'Fiscalizador DT': '<img src="{0}" alt="profile image" />'.format(static('img/fiscalizador_dirc_trab.png')),
        'Trabajador': '<img src="{0}" alt="profile image" />'.format(static('img/trabajador_masculino.png')),
        '': '<img src="{0}" alt="profile image" />'.format(static('img/user_default.png'))
    }

    return perfiles[value]


@register.filter("tag_active")
def tag_active(value):

    if value is True:
        state = '<span class="label label-green">ACTIVA</span>'
    else:
        state = '<span class="label label-danger">INACTIVO</span>'

    return state


@register.filter("tag_active_detail")
def tag_active_detail(value):

    if value is True:
        state = '<span><i class="fas fa-check-square fa-lg text-success"></i> <label>Activo</label></span>'
    else:
        state = '<span><i class="fas fa-minus-square fa-lg text-danger"></i> <label>Inactivo</label></span>'

    return state


@register.filter("tag_examen")
def tag_examen(value):

    if value is True:
        state = '<span class="label label-green">SI</span>'
    else:
        state = '<span class="label label-danger">NO</span>'

    return state


# @register.filter("rut_format")
# def rut_format(value):
#     result = None
#     rut = value.replace('.', '')
#     if value:
#         last = rut[-1:]
#         num = rut[:-1].replace('-', '')
#         format = '{:,}'.format(int(num)).replace(',', '.')

#         result = str(format) + '-' + str(last)

#     return result


@register.filter("tag_activo_fichero")
def tag_activo_fichero(value):

    if value is True:
        state = '<i class="fas fa-check text-success"></i> Activado'
    else:
        state = '<i class="fas fa-ban text-danger"></i> Desactivado'

    return state


@register.filter("show_type_fichero")
def show_type_fichero(path_file):
    html = ''
    if path_file:
        name, extension = os.path.splitext(path_file)
        if extension == '.pdf':
            #html = '<iframe src="'+path_file+'" style="width:100%;height:700px;"></iframe>'
            #html = '<embed src="'+path_file+'#toolbar=0&navpanes=0&scrollbar=0" type="application/pdf" width="100%" height="600px" />'
            html = '<object data="'+path_file+'" type="application/pdf" width="100%" height="400px">' \
                   '<embed src="'+path_file+'" type="application/pdf" width="100%" height="400px">' \
                   '<p>Si no se visualiza el PDF de <a href="'+path_file+'" target="blank">click aquí</a>.</p>' \
                   '</embed></object>'
        else:
            html = '<img src="'+path_file+'" alt="Fichero Imagen" width="100%">'

    return html
