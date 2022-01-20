var tblnegocio;
var modal_title;
var cliente = null;

function getData2() {
    tblnegocio = $('#data-table-default').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/utils/'+cliente+'/negocios/',
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {
            "data": "nombre"
            },
            {"data": "descripcion"},
            {"data": "archivo",
            "render": function(data, type, row, meta){
                data = '<a href="//192.168.0.9:8000/media/' + data + '">' + ' <i class="fa fa-download" aria-hidden="true"></i></a> ';
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

    modal_title = $('.modal-title');
    cliente = document.getElementById("cliente_id").value;

    getData2();

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('negocio_add');
        modal_title.find('span').html('Negocio <small style="font-size: 80%;">Nuevo</small>');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[2].reset();
        $('#myModalnegocio').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Negocio <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblnegocio.cell($(this).closest('td, li')).index();
        var data = tblnegocio.row(tr.row).data();
        $('input[name="action"]').val('negocio_edit');
        $('input[name="id"]' ).val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('Textarea[name="descripcion"]').val(data.descripcion);
        $('file[name="archivo"]').val(data.archivo);
        $('#myModalnegocio').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Negocio <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblnegocio.cell($(this).closest('td, li')).index();
        var data = tblnegocio.row(tr.row).data();
        $('input[name="action"]').val('negocio_delete');
        $('input[name="id"]' ).val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('Textarea[name="descripcion"]').val(data.descripcion);
        $('file[name="archivo"]').val(data.archivo);
        $('#myModalnegocio').modal('show');
    }); 

    $('#myModalnegocio').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('.btnAdd1').on('click', function () {

        $('CrearCreateForm').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalnegocio').modal('hide');
                tblnegocio.ajax.reload();
                $('#myModalplanta').modal('hide');
                tblplanta.ajax.reload();
            }); 
        });

    });

    $('.btnAdd2').on('click', function () {

        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalnegocio').modal('hide');
                tblnegocio.ajax.reload();
                $('#myModalplanta').modal('hide');
                tblplanta.ajax.reload();
            }); 
        });

    });
});