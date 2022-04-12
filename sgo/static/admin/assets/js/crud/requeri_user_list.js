var tblRequeriUser;
var modal_title;
var requerimiento = null;
var enviando = false;
var boton_numero2 = document.getElementById("boton2");
boton_numero2.addEventListener("click", guardar_req_usu);


function getData2() {
    tblRequeriUser = $('#data-table-buttons_wrapper').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/requerimientos/'+requerimiento+'/requirement_users/',
            type: 'POST',
            data: {
                'action': 'searchdata3'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id",
            "render": function(data, type, row, meta){
                data = '<a href="../../../contratos/'+data+'/create_contrato/ ">' + data + ' </a> ';
                return data;
            }},
            {"data": "area_cargo"},
            {"data": "user"},
            {"data": "jefe_area"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> &nbsp &nbsp &nbsp &nbsp';
                    buttons += '<a href="#" rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> &nbsp &nbsp &nbsp &nbsp';
                    buttons += '<a href="#" rel="edit" class="btn btn-info btn-xs btn-flat btnEdit"><i class="fas fa-hospital"></i></a>';
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
    requerimiento = document.getElementById("requerimiento_id").value;

    getData2();

    $('.btnAddRequeUser').on('click', function () {
        $('input[name="action"]').val('requeri_user_add');
        modal_title.find('span').html('Trabajador(es) <small style="font-size: 80%;">Nuevo</small>' );
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        var btn = document.getElementById("boton3");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('form')[2].reset();
        $('#myModalRequerUser').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Trabajador(es) <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblRequeriUser.cell($(this).closest('td, li')).index();
        var data = tblRequeriUser.row(tr.row).data();
        $('form')[2].reset();
        $('input[name="action"]').val('requeri_user_edit');
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
        $('#myModalRequerUser').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Trabajador(es) <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblRequeriUser.cell($(this).closest('td, li')).index();
        var data = tblRequeriUser.row(tr.row).data();
        $('input[name="action"]').val('requeri_user_delete');
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
        $('#myModalRequerUser').modal('show');
    });

    $('#myModalRequerUser').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('.btnAdd3').on('click', function () {

        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalACR').modal('hide');
                tblAreaCargo.ajax.reload();
                $('#myModalRequerUser').modal('hide');
                tblRequeriUser.ajax.reload();
            }); 
        });

    });
});

function guardar_req_usu() { 
    if (enviando == false){
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalRequerTrab').modal('hide');
                tblRequeriUser.ajax.reload();
            });
            enviando = True;   
        });  
    }
  }