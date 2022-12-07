$('#fechaInicioContrato, #fechaInicioAnexo').datepicker({
        format: "yyyy-mm-dd",
        language: 'es'
    });

$('#fechaInicioAnexo').datepicker({
        startDate: '+5d',
        endDate: '+35d',
    });
    
    

    function sumarDias(fecha, dias){
        fecha.setDate(fecha.getDate() + dias);
        return fecha;
      }

   
// var inicio = new Date($('#UltimoAnexo').val());
// var fin = new Date($('#f_termino').val()); 
var fecha_maxima = document.getElementById("f_termino").value
var formato_fmax = new Date(fecha_maxima);
var sum_fecha_maxima = sumarDias(formato_fmax, 1);

 
var fecha_minima = document.getElementById("UltimoAnexo").value
var formato_fmin = new Date(fecha_minima);
var sum_fecha_minima = sumarDias(formato_fmin, 2);



 
$('#fechaInicioAnexo').datepicker('clearDates');
$('#fechaInicioAnexo').datepicker("setStartDate", new Date(sum_fecha_minima))
$('#fechaInicioAnexo').datepicker('clearDates');
$('#fechaInicioAnexo').datepicker("setEndDate", new Date(sum_fecha_maxima))

