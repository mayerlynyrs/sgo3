var tblProfesionUser;
var modal_title;
var user = null;


function getData2() {
    tblProfesionUser = $('#data-table-buttons_wrapper').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/users/'+user+'/profesion_users/',
            type: 'POST',
            data: {
                'action': 'searchdata3'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "egreso"},
            {"data": "institucion"},
            {"data": "profesion"},
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

    $('#egreso').datepicker({
        format: "yyyy-mm-dd",
        language: 'es'
    });
    
    modal_title = $('.modal-title');
    user = document.getElementById("user_id").value;

    getData2();

    $('.btnAddProfes').on('click', function () {
        $('input[name="action"]').val('profesion_add');
        modal_title.find('span').html('Profesión <small style="font-size: 80%;">Nuevo</small>' );
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[2].reset();
        $('#myModalProfesionUser').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Profesión <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblProfesionUser.cell($(this).closest('td, li')).index();
        var data = tblProfesionUser.row(tr.row).data();
        $('form')[2].reset();
        $('input[name="action"]').val('profesion_edit');
        $('input[name="id"]' ).val(data.id);
        $('input[name="egreso"]').val(data.egreso);
        $('input[name="institucion"]').val(data.institucion);
        $('select[name="profesion"]').val(data.profesion_id);
        $('#myModalProfesionUser').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Profesión <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblProfesionUser.cell($(this).closest('td, li')).index();
        var data = tblProfesionUser.row(tr.row).data();
        $('input[name="action"]').val('profesion_delete');
        $('input[name="id"]').val(data.id);
        $('input[name="egreso"]').val(data.egreso);
        $('input[name="institucion"]').val(data.institucion);
        $('select[name="profesion"]').val(data.profesion_id);
        $('#myModalProfesionUser').modal('show');
    }); 

    $('#myModalProfesionUser').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('.btnAdd3').on('click', function () {

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