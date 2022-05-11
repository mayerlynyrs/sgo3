var tblSalud;
var modal_title;

function getData() {
    tblSalud = $('#data-table-default').DataTable({
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
            {"data": "nombre"},
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
        modal_title.find('span').html('Sistema de Previsión <small style="font-size: 80%;">Nuevo</small>');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[0].reset();
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('#myModalSalud').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Sistema de Previsión <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblSalud.cell($(this).closest('td, li')).index();
        var data = tblSalud.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]' ).val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalSalud').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Sistema de Previsión <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblSalud.cell($(this).closest('td, li')).index();
        var data = tblSalud.row(tr.row).data();
        $('input[name="action"]').val('delete');
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalSalud').modal('show');
    });

    $('#myModalSalud').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        console.log(FormData);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalSalud').modal('hide');
            tblSalud.ajax.reload();
        });   
    });
});