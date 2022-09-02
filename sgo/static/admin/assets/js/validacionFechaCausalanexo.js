$('#fechaInicioContrato, #fechaInicioAnexo').datepicker({
        format: "yyyy-mm-dd",
        language: 'es'
    });

$('#fechaInicioAnexo').datepicker({
        startDate: '+5d',
        endDate: '+35d',
    }); 

   
var inicio = new Date($('#UltimoAnexo').val());
var fin = new Date($('#f_termino').val()); 
 
$('#fechaInicioAnexo').datepicker('clearDates');
$('#fechaInicioAnexo').datepicker("setStartDate", new Date(inicio))
$('#fechaInicioAnexo').datepicker('clearDates');
$('#fechaInicioAnexo').datepicker("setEndDate", new Date(fin))

