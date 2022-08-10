
$(function () {

    var fecha_manxima = document.getElementById("f_termino").value
    var fecha_minima = document.getElementById("f_inicio").value 

    
    $('#fecha_inicio, #fecha_solicitud , #fecha_termino').datepicker({
        format: "yyyy-mm-dd",
        language: 'es'
    });

    $('#fecha_solicitud').datepicker({
        startDate: '+6d',
        endDate: '+36d',
    });

    $('#fecha_termino').datepicker({
        startDate: '+6d',
        endDate: '+36d',
    });
    

    $('#fecha_inicio').datepicker("setStartDate", new Date(fecha_minima))
    $('#fecha_inicio').datepicker("setEndDate", new Date(fecha_manxima))
    $('#fecha_termino').datepicker("setStartDate", new Date(fecha_minima))
    $('#fecha_termino').datepicker("setEndDate", new Date(fecha_manxima))
});

