var tblRevExaSolicit;
var modal_title;


function getData() {
    tblRevExaSolicit = $('#data-table-default').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "trabajador"},
            {"data": "requerimiento"},
            {"data": "planta"},
            {"data": "bateria"},
            {"data": "examen[ <br> ].nombre"},
            {"data": "id"},
        ],
        buttons: [{
            extend: 'excelHtml5',
            text: 'hola',
            titleAttr: 'Exportar a Excel',
            className: 'btn btn-success'

        }],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" data-toggle="modal" data-target="#myModalRevExam" rel="agg" title="Evaluar" class="btn btn-primary btn-xs btn-flat btnAgg"><i class="fas fa-fw fa-newspaper"></i></a>  &nbsp &nbsp';
                    // var buttons = '<a href="#" rel="edit" title="Editar" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a>  &nbsp &nbsp';
                    // buttons += '<a href="#" rel="delete" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> &nbsp &nbsp';
                    // buttons += '<a href="#" data-toggle="modal" data-target="#myModalEvaluacion" rel="agg" title="Evaluar" class="btn btn-primary btn-xs btn-flat btnAgg"><i class="fas fa-fw fa-newspaper"></i></a>';
                    buttons += '<a href="#" data-toggle="modal" data-target="#myModalExaTraba" rel="ver" title="Ver Examénes" class="btn btn-lime btn-xs btn-flat btnAgg"><i class="fas fa-book-medical"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    
   
    modal_title = $('.modal-title');

    getData();

    $('#data-table-default tbody').on('click', 'a[rel="agg"]', function (){
        $('input[name="action"]').val('evaluacion_add');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        var tr = tblRevExaSolicit.cell($(this).closest('td, li')).index();
        var data = tblRevExaSolicit.row(tr.row).data();   
        modal_title.find('span').html('Aprobar/Rechazar <small style="font-size: 90%;"> Solicitud </small>');
        $('form')[0].reset();
        $('input[name="id"]' ).val(data.id);
        $('input[name="user_id"]').val(data.user_id);
        $('select[name="planta"]').val(data.planta).trigger("change");
        $('select[name="cargo"]').val(data.cargo).trigger("change");
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('select[name="bateria"]').val(data.bateria).trigger("change");
        $('select[name="centromedico"]').val(data.centro).trigger("change");
        
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        
       
        $('#myModalRevExam').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="ver"]', function (){
    
        
        modal_title.find('i').removeClass().addClass('fas fa-ver');
        var tr = tblRevExaSolicit.cell($(this).closest('td, li')).index();
        var data = tblRevExaSolicit.row(tr.row).data();
        modal_title.find('span').html('Examen(es) de ' + data.trabajador);
        $('input[name="rut"]' ).val(data.rut);
        $('input[name="action"]').val('ver');
        $('input[name="id"]' ).val(data.id);
        $('select[name="estado"]').val(data.estado).trigger("change");
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('input[name="fecha_ingreso_estimada"]').val(data.fecha_ingreso_estimada);
        $('input[name="fecha_agenda_evaluacion"]').val(data.fecha_agenda_evaluacion);
        $('select[name="planta"]').val(data.planta).trigger("change");
        $('select[name="cargo"]').val(data.cargo).trigger("change");
        $('select[name="bateria"]').val(data.bateria).trigger("change");
        $('select[name="centromedico"]').val(data.centro).trigger("change");
        $('select[name="evaluacion"]').val(data.evaluacion).trigger("change");
        $('select[name="psico"]').val(data.psico).trigger("change");
        $('input:checkbox[name=Hal2]').attr('checked',data.Hal2);  
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('textarea[name="obs"]').val(data.obs);
        // var btn = document.getElementById("btn-guardar");
        // btn.style.borderColor= '#153264';
        // btn.style.backgroundColor= '#153264';
        // btn.innerHTML = 'Editar';
        $('#myModalExaTraba').modal('show');
    });

    $('#myModalExaTraba').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        console.log(FormData);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalExaTraba').modal('hide');
            $('#myModalRevExam').modal('hide');
            tblRevExaSolicit.ajax.reload();
        });   
    });
});