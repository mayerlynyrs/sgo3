var tblContact;
var modal_title;
var user = null;
var enviando = false;
var boton_numero1 = document.getElementById("boton");
boton_numero1.addEventListener("click", guardar_contacto);

function getData() {
    tblContact = $('#data-table-default').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/users/'+user+'/contactos/',
            type: 'POST',
            data: {
                'action': 'searchdata2'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "nombre"},
            {"data": "telefono"},
            {"data": "parentesco"},
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
    user = document.getElementById("user_id").value;

    getData();

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('contacto_add');
        modal_title.find('span').html('Contacto <small style="font-size: 80%;">Nuevo</small>');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[1].reset();
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('#myModalcontacto').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Contacto <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblContact.cell($(this).closest('td, li')).index();
        var data = tblContact.row(tr.row).data();
        $('input[name="action"]').val('contacto_edit');
        $('input[name="id"]' ).val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="telefono"]').val(data.telefono);
        $('select[name="parentesco"]').val(data.parentesco_id).trigger("change");
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalcontacto').modal('show');
        return data;
    });

    $('#data-table-default tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Contacto <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblContact.cell($(this).closest('td, li')).index();
        var data = tblContact.row(tr.row).data();
        $('input[name="action"]').val('contacto_delete');
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="telefono"]').val(data.telefono);
        $('select[name="parentesco"]').val(data.parentesco_id).trigger("change");
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalcontacto').modal('show');
    }); 

    $('#myModalcontacto').on('shown.bs.modal', function () {
        // $('form')[0].reset();
    });

    $('.btnAdd1').on('click', function () {

        $('CrearUsuarioForm').on('submit', function (e) {
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

function guardar_contacto() { 
    if (enviando == false){
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalcontacto').modal('hide');
                tblContact.ajax.reload();
            });
            enviando = True;   
        });  
    }
  }