def fecha_a_letras(fecha):
    if fecha.month == 1:
        mes = 'Enero'
    elif fecha.month == 2:
        mes = 'Febrero'
    elif fecha.month == 3:
        mes = 'Marzo'
    elif fecha.month == 4:
        mes = 'Abril'
    elif fecha.month == 5:
        mes = 'Mayo'
    elif fecha.month == 6:
        mes = 'Junio'
    elif fecha.month == 7:
        mes = 'Julio'
    elif fecha.month == 8:
        mes = 'Agosto'
    elif fecha.month == 9:
        mes = 'Septiembre'
    elif fecha.month == 10:
        mes = 'Octubre'
    elif fecha.month == 11:
        mes = 'Noviembre'
    elif fecha.month == 12:
        mes = 'Diciembre'
    fecha_palabras = str(fecha.day) + ' de ' + mes + ' de ' + str(fecha.year)
    return fecha_palabras
  