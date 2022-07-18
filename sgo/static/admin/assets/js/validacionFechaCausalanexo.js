$('#fechaInicioContrato, #fechaInicioAnexo').datepicker({
        format: "yyyy-mm-dd",
        language: 'es'
    });

    $('#fechaInicioAnexo').datepicker({
        startDate: '+5d',
        endDate: '+35d',
    }); 
    var date = new Date($('#fechaInicioContrato').val());
    var causal = document.getElementById('id_causalanexo').value;
    
    if (causal == 2 || causal == 5){
        var dias = 90; // Número de días a agregar
    }
    else if (causal == 3 || causal == 4 ){
        var dias = 180;
    }else{
        dias = 700;
    }
    // console.log(causal);
    date.setDate(date.getDate() + dias);
    var currentMonth = date.getMonth();
    var currentDate = date.getDate();
    var currentYear = date.getFullYear();
            
    if (date != "Invalid Date"){
        var fin = date.toISOString().slice(0, 10);
        var inicio = new Date($('#UltimoAnexo').val());
        if (inicio == "Invalid Date"){
            var inicio = new Date($('#fechaInicioContrato').val());
        }
        // console.log('inicio', inicio)
        $('#fechaInicioAnexo').datepicker('clearDates');
        $('#fechaInicioAnexo').datepicker("setStartDate", new Date(inicio))
        $('#fechaInicioAnexo').datepicker('clearDates');
        $('#fechaInicioAnexo').datepicker("setEndDate", new Date(fin))
    }
