var tblSolicitudes;
var modal_title;

function getData() {
    tblSolicitudes = $('#data-table-default').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata5'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "user"},
            {"data": "fecha_ingreso_estimada"},
            {"data": "planta_nombre"},
            {"data": "tipo_examen"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> &nbsp &nbsp &nbsp &nbsp';
                    buttons += '<a href="#" rel="delete" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
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

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Solicitud' );
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[0].reset();
        var btn = document.getElementById("btn-guardar");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('#mySolicitudes').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Editar Solicitud');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblSolicitudes.cell($(this).closest('td, li')).index();
        var data = tblSolicitudes.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]' ).val(data.id);
        $('select[name="requerimiento"]').val(data.requerimiento).trigger("change");
        $('select[name="trabajador"]').val(data.trabajador).trigger("change");
        $('select[name="cargo"]').val(data.cargo).trigger("change");
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('input[name="fecha_ingreso_estimada"]').val(data.fecha_ingreso_estimada);
        $('select[name="planta"]').val(data.planta).trigger("change");
        $('select[name="evaluacion"]').val(data.evaluacion).trigger("change");
        $('input:checkbox[name=Hal2]').attr('checked',data.Hal2);  
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('textarea[name="obs"]').val(data.obs);
        var btn = document.getElementById("btn-guardar");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#mySolicitudes').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('¿Desea Eliminar solicitud?');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblSolicitudes.cell($(this).closest('td, li')).index();
        var data = tblSolicitudes.row(tr.row).data();
        $('input[name="action"]').val('delete');
        $('input[name="id"]' ).val(data.id);
        $('select[name="requerimiento"]').val(data.requerimiento).trigger("change");
        $('select[name="trabajador"]').val(data.trabajador).trigger("change");
        $('select[name="cargo"]').val(data.cargo).trigger("change");
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('input[name="fecha_ingreso_estimada"]').val(data.fecha_ingreso_estimada);
        $('select[name="planta"]').val(data.planta).trigger("change");
        $('select[name="evaluacion"]').val(data.evaluacion).trigger("change");
        $('input:checkbox[name=Hal2]').attr('checked',data.Hal2);  
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('textarea[name="obs"]').val(data.obs);
        var btn = document.getElementById("btn-guardar");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#mySolicitudes').modal('show');
    });

    $('#mySolicitudes').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        console.log(FormData);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#mySolicitudes').modal('hide');
            tblSolicitudes.ajax.reload();
        });   
    });
});