$(function () {

            var d = new Date(),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear()
            console.log(day, month, year);
            var anio = year - 18;
            console.log(anio);
            var fecha_validada = anio+"-"+month+"-"+day;



            jQuery('#fecha').datetimepicker({
                timepicker : false,
                format:'Y-m-d',
                maxDate: fecha_validada
                
              });


            });
