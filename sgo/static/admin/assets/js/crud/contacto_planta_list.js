var tblContactoPlanta;
var modal_title;
var cliente = null;
var enviando = false;
var boton_numero3 = document.getElementById("boton3");
boton_numero3.addEventListener("click", guardar_contacto_planta);


function getData4() {
    tblContactoPlanta = $('#data-table-responsive').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/clientes/'+cliente+'/planta_contactos/',
            type: 'POST',
            data: {
                'action': 'searchdata4'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "nombres"},
            {"data": "apellidos"},
            {"data": "planta"},
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
    cliente = document.getElementById("cliente_id").value;

    getData4();

    $('.btnAddRequeUser').on('click', function () {
        $('input[name="action"]').val('cp_contacto_add');
        modal_title.find('span').html('Trabajador(es) <small style="font-size: 80%;">Nuevo</small>' );
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        var tr = tblPlanta.cell($(this).closest('td, li')).index();
        var data = tblPlanta.row(tr.row).data();
        $('input[name="planta_id"]').val(data.id);
        console.log(data.id);
        var btn = document.getElementById("boton3");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('form')[2].reset();
        $('#myModalContactoPlanta').modal('show');
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Trabajador(es) <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblContactoPlanta.cell($(this).closest('td, li')).index();
        var data = tblContactoPlanta.row(tr.row).data();
        $('form')[2].reset();
        $('input[name="action"]').val('cp_contacto_edit');
        $('input[name="id"]' ).val(data.id);
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('textarea[name="descripcion"]').val(data.descripcion);
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('input[name="pension"]').val(data.pension);
        $('select[name="user"]').val(data.user_id).trigger("change");
        $('select[name="jefe_area"]').val(data.jefe_area_id).trigger("change");
        var btn = document.getElementById("boton3");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalContactoPlanta').modal('show');
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Trabajador(es) <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblContactoPlanta.cell($(this).closest('td, li')).index();
        var data = tblContactoPlanta.row(tr.row).data();
        $('input[name="action"]').val('cp_contacto_delete');
        $('input[name="id"]').val(data.id);
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('textarea[name="descripcion"]').val(data.descripcion);
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('input[name="pension"]').val(data.pension);
        $('select[name="user"]').val(data.user_id).trigger("change");
        $('select[name="jefe_area"]').val(data.jefe_area_id).trigger("change");
        var btn = document.getElementById("boton3");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalContactoPlanta').modal('show');
    });

    $('#myModalContactoPlanta').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('.btnAdd3').on('click', function () {

        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalplanta').modal('hide');
                tblPlanta.ajax.reload();
                $('#myModalContactoPlanta').modal('hide');
                tblContactoPlanta.ajax.reload();
            }); 
        });

    });
});

function guardar_contacto_planta() { 
    if (enviando == false){
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalContactoPlanta').modal('hide');
                tblContactoPlanta.ajax.reload();
            });
            enviando = True;   
        });  
    }
  }