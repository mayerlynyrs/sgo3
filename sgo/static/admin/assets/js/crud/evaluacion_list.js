var tblExamenes;
var modal_title;
var trabajador = null;
var MEDIA_URL;
var enviando = false;
var boton_numero4 = document.getElementById("boton3");
boton_numero4.addEventListener("click", guardar_evaluacion); 

function getdata5() {
    tblExamenes = $('#data-table-responsive').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/users/'+trabajador+'/evaluacion_trabajadores/',
            type: 'POST',
            data: {
                'action': 'searchdata5'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "tipoexamen"},
            {"data": "resultado"},
            {"data": "fecha_termino"},
            {"data": "archivo",
            "render": function(data, type, row, meta){
                data = '<a href="../../../media/' + data + '">' + ' <i  class="fa fa-download" title="Descargar" aria-hidden="true"></i></a> ';
                return data;
            }},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="delete" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    trabajador = document.getElementById("trabajador_id").value;
    console.log(trabajador);

    
    var getDate = function (input) {
        return new Date(input.date.valueOf());
    }

    $('#fecha_examen, #fecha_vigencia').datepicker({
        format: "yyyy-mm-dd",
        language: 'es'
    });
    
    $('#fecha_vigencia').datepicker({
        startDate: '+6d',
        endDate: '+36d',
    });
    
    $('#fecha_examen').datepicker({
        startDate: '+5d',
        endDate: '+35d',
    }).on('changeDate',
        function (selected) {
            $('#fecha_vigencia').datepicker('clearDates');
            $('#fecha_vigencia').datepicker('setStartDate', getDate(selected));
        });
    getdata5();

    $('.btnAddExamen').on('click', function () {
        $('input[name="action"]').val('evaluacion_add');
        modal_title.find('span').html('Examen <small style="font-size: 80%;">Nuevo</small>' );
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[4].reset();
        var btn = document.getElementById("boton3");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('#myModalEvaluacion').modal('show');
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Examen <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblExamenes.cell($(this).closest('td, li')).index();
        var data = tblExamenes.row(tr.row).data();
        $('form')[4].reset();
        $('input[name="action"]').val('evaluacion_edit');
        $('input[name="id"]' ).val(data.id);
        $('input[name="fecha_examen"]').val(data.fecha_examen);
        $('input[name="fecha_vigencia"]').val(data.fecha_vigencia);
        $('input[name="valor_examen"]').val(data.valor_examen);
        $('select[name="examen"]').val(data.examen_id).trigger("change");
        $('select[name="resultado"]').val(data.resultado).trigger("change");
        $('select[name="planta"]').val(data.planta).trigger("change");
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('file[name="archivo_0"]').val(data.archivo);
        $('textarea[name="descripcion"]').val(data.descripcion);
        var btn = document.getElementById("boton3");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalEvaluacion').modal('show');
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Archivo <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblExamenes.cell($(this).closest('td, li')).index();
        var data = tblExamenes.row(tr.row).data();
        $('input[name="action"]').val('evaluacion_delete');
        $('input[name="id"]').val(data.id);
        $('input[name="fecha_examen"]').val(data.fecha_examen);
        $('input[name="fecha_vigencia"]').val(data.fecha_vigencia);
        $('input[name="valor_examen"]').val(data.valor_examen);
        $('select[name="examen"]').val(data.examen_id).trigger("change");
        $('select[name="resultado"]').val(data.resultado).trigger("change");
        $('select[name="planta"]').val(data.planta).trigger("change");
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('file[name="archivo"]').val(data.archivo);
        $('textarea[name="descripcion"]').val(data.descripcion);
        var btn = document.getElementById("boton3");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalEvaluacion').modal('show');
    }); 

    $('#myModalEvaluacion').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });
});

function guardar_evaluacion() { 
    if (enviando == false){ 
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalEvaluacion').modal('hide');
                tblExamenes.ajax.reload();
            });
            enviando = True; 
        });  
    }
  }