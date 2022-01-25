
$(function () {

    
    var getDate = function (input) {
        return new Date(input.date.valueOf());
    }

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
            var date = new Date($('#fecha_inicio').val());   
            var causal = document.getElementById("id_causal").value;
    
            if (causal == 2 || causal == 5){
                var dias = 90; // Número de días a agregar
            }
            else if (causal == 3 || causal == 4 ){
                var dias = 180;
            }else{
                dias = 700;
            }
            console.log(causal);
            date.setDate(date.getDate() + dias);
            var currentMonth = date.getMonth();
            var currentDate = date.getDate();
            var currentYear = date.getFullYear();
            var fecha = date.toISOString().slice(0, 10);   
            var fechaformat = fecha.split('-');
            var fechaformateada = fechaformat[0] +","+fechaformat[1]+","+fechaformat[2];
            $('#fecha_termino').datepicker('clearDates');
            $('#fecha_termino').datepicker('setStartDate', getDate(selected));
            $('#fecha_termino').datepicker('clearDates');
            $('#fecha_termino').datepicker("setEndDate", new Date(fechaformateada))
            
        });
    
});

function getval(sel)
{
    $('#fecha_inicio').datepicker('setDate', null);
    $('#fecha_termino').datepicker('setDate', null);
}

