var tblContactoPlanta;
var modal_title;
var cliente = null;
var enviando = false;
var boton_numero3 = document.getElementById("boton6");
var boton_numero8 = document.getElementById("boton5");
boton_numero3.addEventListener("click", guardar_contacto_planta);
boton_numero8.addEventListener("click", guardar_contacto_planta);

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


    $('#data-table-responsive tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Trabajador(es) <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblContactoPlanta.cell($(this).closest('td, li')).index();
        var data = tblContactoPlanta.row(tr.row).data();
        $('input[name="action"]').val('cp_contacto_edit');
        $('input[name="id"]' ).val(data.id);
        $('input[name="nombres"]').val(data.nombres);
        $('input[name="apellidos"]').val(data.apellidos);
        $('input[name="rut"]').val(data.rut);
        $('input[name="fecha_nacimiento"]').val(data.fecha_nacimiento);
        $('select[name="relacion"]').val(data.relacion).trigger("change");
        $('input[name="telefono"]').val(data.telefono);
        $('input[name="email"]').val(data.email);
        $('input[name="user_id"]').val(data.user_id);
        var btn = document.getElementById("boton6");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalContactoPlantaE').modal('show');
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Trabajador(es) <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblContactoPlanta.cell($(this).closest('td, li')).index();
        var data = tblContactoPlanta.row(tr.row).data();
        $('input[name="action"]').val('cp_contacto_delete');
        $('input[name="id"]' ).val(data.id);
        $('input[name="nombres"]').val(data.nombres);
        $('input[name="apellidos"]').val(data.apellidos);
        $('input[name="rut"]').val(data.rut);
        $('input[name="fecha_nacimiento"]').val(data.fecha_nacimiento);
        $('select[name="relacion"]').val(data.relacion).trigger("change");
        $('input[name="telefono"]').val(data.telefono);
        $('input[name="email"]').val(data.email);
        $('input[name="user_id"]').val(data.user_id);

        var btn = document.getElementById("boton6");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalContactoPlantaE').modal('show');
    });

    $('#myModalContactoPlantaE').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('.btnAdd3').on('click', function () {

        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalContactoPlantaE').modal('hide');
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
                $('#myModalContactoPlantaE').modal('hide');
                $('#myModalContactoPlanta').modal('hide');
                tblContactoPlanta.ajax.reload();
            });
            enviando = True;   
        });  
    }
  }