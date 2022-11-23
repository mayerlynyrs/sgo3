
from datetime import datetime
import pythoncom
from contratos.models import Plantilla
from requerimientos.fecha_a_palabras import fecha_a_letras
from contratos.models import  Contrato, DocumentosContrato
from docxtpl import DocxTemplate 
import os
from docx2pdf import convert
import win32com.client
from django.conf import settings

def finiquito(contrato2):
    contrato = Contrato.objects.get(pk=contrato2)
    if(contrato.tipo_documento.id == 8):
            sueldo_base = round(contrato.sueldo_base / 30)
            gratificacion = round(sueldo_base * 0.25)
            total_haberes_imponibles = sueldo_base + gratificacion
            feriado_proporcional = round((sueldo_base * 1.25) / 30)
            total_no_haberes_imponibles = feriado_proporcional
            total_haberes = total_haberes_imponibles + total_no_haberes_imponibles
            pago_liquido = contrato.valores_diario.valor_diario + feriado_proporcional 
            salud = round(total_haberes_imponibles * 0.07)
            afp = round(total_haberes_imponibles * (contrato.trabajador.afp.tasa / 100))
            total_descuento = salud + afp

            plant_template = Contrato.objects.values_list('planta', flat=True).get(pk=contrato.id, status=True)
            formato = Plantilla.objects.values('archivo', 'abreviatura', 'tipo_id').filter(plantas=plant_template, tipo_id=11)
            for formt in formato:
                now = datetime.now()
                doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT + '/' + formt['archivo']))
            
                context = { 'fecha_pago_contrato': fecha_a_letras(contrato.fecha_pago),
                            'nombre_trabajador': contrato.trabajador.first_name.title() + ' '+ contrato.trabajador.last_name.title(),
                            'cargo_postulante': contrato.requerimiento_trabajador.area_cargo.cargo.nombre.title(),
                            'fecha_inicio_contrato': fecha_a_letras(contrato.fecha_inicio),
                            'fecha_termino_contrato' : fecha_a_letras(contrato.fecha_termino),
                            'periodo_contrato': contrato.fecha_termino.strftime(" %b, %Y"),
                            'sueldo_base': sueldo_base,
                            'gratificacion_mensual': gratificacion,
                            'bono_gestion': '',
                            'total_imponibles': total_haberes_imponibles,
                            'feriado_proporcional': feriado_proporcional,
                            'total_no_imponibles' : total_no_haberes_imponibles,
                            'total_haberes' : total_haberes,
                            'total_liquido' : pago_liquido,
                            'fondo_pension' : afp,
                            'aporte_salud' : salud,
                            'total_leyes_sociales': total_descuento,
                            'total_descuentos' : total_descuento,
                            'rut_trabajador' : contrato.trabajador.rut,

                            }
                
                doc.render(context)
                path = os.path.join(settings.MEDIA_ROOT + '/contratos/')
                doc.save(path + str(contrato.trabajador.rut) + "_" + formt['abreviatura'] + "_" + str(contrato.id)  + '.docx')
                win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
                convert(path + str(contrato.trabajador.rut) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".docx", path +  str(contrato.trabajador.rut) + "_" + formt['abreviatura'] + "_" +  str(contrato.id) + ".pdf")
                url = str(contrato.trabajador.rut) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + ".pdf"
                os.remove(path + str(contrato.trabajador.rut) + "_" + formt['abreviatura'] + "_" + str(contrato.id) + '.docx')
                doc_contrato = DocumentosContrato(contrato=contrato, archivo=url )
                doc_contrato.tipo_documento_id = 10
                doc_contrato.save()