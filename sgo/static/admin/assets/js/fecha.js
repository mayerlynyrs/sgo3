$(function () {

    var date = new Date($('#fecha').val());
            var d = new Date(),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear()
            console.log(day, month, year);
            var anio = year - 18;
            console.log(anio);
            var fecha_validada = anio+","+month+","+day;
            
    
            $('#fecha').datepicker("setEndDate", new Date(fecha_validada))

    $('#fecha').datepicker({
        format: "dd-mm-yyyy",
        language: 'es',
        
    });



});