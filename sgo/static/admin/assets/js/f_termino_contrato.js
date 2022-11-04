
$(function () {
    fecha_termino.disabled = true;

    
    var getDate = function (input) {
        return new Date(input.date.valueOf());
    }

    var fecha_maxima = document.getElementById("f_termino").value
    var fecha_minima = document.getElementById("f_inicio").value

    function sumarDias(fecha, dias){
        fecha.setDate(fecha.getDate() + dias);
        return fecha;
      }

    //   Sumar un dia a la fecha_maxima (f_termino) para que el calendario tome la fecha que se requiere
      var formato_fmax = new Date(fecha_maxima);
      var sum_fecha_maxima = sumarDias(formato_fmax, 1);

      //   Sumar un dia a la fecha_minima (f_inicio) para que el calendario tome la fecha que se requiere
        var formato_fmin = new Date(fecha_minima);
        var sum_fecha_minima = sumarDias(formato_fmin, 1);
    
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
    
    $('#fecha_inicio').datepicker({
        startDate: '+5d',
        endDate: '+35d',
    }).on('changeDate',
        function (selected) {
            fecha_termino.disabled = false;
            var date = new Date($('#fecha_inicio').val());
            var currentMonth = date.getMonth();
            var currentDate = date.getDate();
            var currentYear = date.getFullYear();
            
            if (date != "Invalid Date"){
                $('#fecha_termino').datepicker('clearDates');
                $('#fecha_termino').datepicker('setStartDate', getDate(selected));
                $('#fecha_termino').datepicker('clearDates');
                $('#fecha_termino').datepicker("setEndDate", new Date(sum_fecha_maxima))
            }
            
            
        });
    

    $('#fecha_inicio').datepicker("setStartDate", new Date(sum_fecha_minima))
    $('#fecha_inicio').datepicker("setEndDate", new Date(sum_fecha_maxima))
});

