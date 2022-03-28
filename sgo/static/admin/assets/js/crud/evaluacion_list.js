var tblExamenes;
var modal_title;
var user = null;
var MEDIA_URL;

function getdata5() {
    tblExamenes = $('#data-table-responsive').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/users/'+user+'/evaluacion_users/',
            type: 'POST',
            data: {
                'action': 'searchdata5'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "examen"},
            {"data": "resultado"},
            {"data": "fecha_vigencia"},
            {"data": "archivo",
            "render": function(data, type, row, meta){
                data = '<a href="../../../media/' + data + '">' + ' <i class="fa fa-download" aria-hidden="true"></i></a> ';
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
                    var buttons = '<a href="#" rel="edit" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> &nbsp &nbsp &nbsp &nbsp';
                    buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    
    var getDate = function (input) {
        return new Date(input.date.valueOf());
    }

    $('#fecha_examen, #fecha_vigencia').datepicker({
        format: "dd-mm-yyyy",
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
        $('form')[3].reset();
        var btn = document.getElementById("boton4");
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('#myModalEvaluacion').modal('show');
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Examen <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblExamenes.cell($(this).closest('td, li')).index();
        var data = tblExamenes.row(tr.row).data();
        $('form')[3].reset();
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
        var btn = document.getElementById("boton4");
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
        var btn = document.getElementById("boton4");
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalEvaluacion').modal('show');
    }); 

    $('#myModalEvaluacion').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('.btnAdd5').on('click', function () {

        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalcontacto').modal('hide');
                tblContact.ajax.reload();
                $('#myModalProfesionUser').modal('hide');
                tblProfesionUser.ajax.reload();
                $('#myModalEvaluacion').modal('hide');
                tblExamenes.ajax.reload();
                $('#myModalArchivoUser').modal('hide');
                tblArchivoUser.ajax.reload();
            }); 
        });

    });
});