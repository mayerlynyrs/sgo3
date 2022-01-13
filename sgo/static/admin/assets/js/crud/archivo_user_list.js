var tblArchivoUser;
var modal_title;
var user = null;

function getData3() {
    tblArchivoUser = $('#data-table-responsive').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/users/'+user+'/archivo_users/',
            type: 'POST',
            data: {
                'action': 'searchdata4'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "tipo_archivo"},
            {"data": "archivo"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    // buttons = '<a href="#" rel="edit" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> &nbsp &nbsp &nbsp &nbsp';
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
    user = document.getElementById("user_id").value;

    getData3();

    $('.btnAddArchi').on('click', function () {
        $('input[name="action"]').val('archivo_add');
        modal_title.find('span').html('Archivo <small style="font-size: 80%;">Nuevo</small>' );
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[3].reset();
        $('#myModalArchivoUser').modal('show');
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Archivo <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblArchivoUser.cell($(this).closest('td, li')).index();
        var data = tblArchivoUser.row(tr.row).data();
        $('form')[3].reset();
        $('input[name="action"]').val('archivo_edit');
        $('input[name="id"]' ).val(data.id);
        $('select[name="tipo_archivo"]').val(data.tipo_archivo_id);
        $('file[name="archivo"]').val(data.archivo);
        $('#myModalArchivoUser').modal('show');
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Archivo <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblArchivoUser.cell($(this).closest('td, li')).index();
        var data = tblArchivoUser.row(tr.row).data();
        $('input[name="action"]').val('archivo_delete');
        $('input[name="id"]').val(data.id);
        $('select[name="tipo_archivo"]').val(data.tipo_archivo_id);
        $('file[name="archivo"]').val(data.archivo);
        $('#myModalArchivoUser').modal('show');
    }); 

    $('#myModalArchivoUser').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('.btnAdd4').on('click', function () {

        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalcontacto').modal('hide');
                tblContact.ajax.reload();
                $('#myModalProfesionUser').modal('hide');
                tblProfesionUser.ajax.reload();
                $('#myModalArchivoUser').modal('hide');
                tblArchivoUser.ajax.reload();
            }); 
        });

    });
});