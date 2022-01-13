var tblplanta;
var modal_title;
var cliente = null;

function getData() {
    tblplanta = $('#data-table-buttons_wrapper').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/utils/'+cliente+'/plantas/',
            type: 'POST',
            data: {
                'action': 'searchdata2'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "nombre"},
            {"data": "rut"},
            {"data": "negocio"},
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

    getData();

    $('.btnAddplanta').on('click', function () {
        $('input[name="action"]').val('planta_add');
        modal_title.find('span').html('Planta <small style="font-size: 80%;">Nuevo</small>');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[2].reset();
        $('#myModalplanta').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Planta <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblplanta.cell($(this).closest('td, li')).index();
        var data = tblplanta.row(tr.row).data();
        $('input[name="action"]').val('planta_edit');
        $('input[name="id"]' ).val(data.id);
        $('select[name="negocio"]').val(data.negocio);
        $('input[name="rut"]').val(data.rut);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="telefono"]').val(data.telefono);
        $('input[name="email"]').val(data.email);
        $('select[name="region"]').val(data.region_id);
        $('select[name="provincia"]').val(data.provincia_id);
        $('select[name="ciudad"]').val(data.ciudad_id);
        $('input[name="direccion"]').val(data.direccion);
        $('select[name="bono"]').val(data.bono);
        $('select[name="gratificacion"]').val(data.gratificacion_id);
        $('select[name="examen"]').val(data.examen_id);
        $('input[name="rut_gerente"]').val(data.rut_gerente);
        $('input[name="nombre_gerente"]').val(data.nombre_gerente);
        $('input[name="direccion_gerente"]').val(data.direccion_gerente);
        $('#myModalplanta').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Negocio <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblplanta.cell($(this).closest('td, li')).index();
        var data = tblplanta.row(tr.row).data();
        $('input[name="action"]').val('planta_delete');
        $('input[name="id"]' ).val(data.id);
        $('select[name="negocio"]').val(data.negocio);
        $('input[name="rut"]').val(data.rut);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="telefono"]').val(data.telefono);
        $('input[name="email"]').val(data.email);
        $('select[name="region"]').val(data.region_id);
        $('select[name="provincia"]').val(data.provincia_id);
        $('select[name="ciudad"]').val(data.ciudad_id);
        $('input[name="direccion"]').val(data.direccion);
        $('select[name="bono"]').val(data.bono_id);
        $('select[name="gratificacion"]').val(data.gratificacion_id);
        $('select[name="examen"]').val(data.examen_id);
        $('input[name="rut_gerente"]').val(data.rut_gerente);
        $('input[name="nombre_gerente"]').val(data.nombre_gerente);
        $('input[name="direcccion_gerente"]').val(data.direcccion_gerente);
        $('#myModalplanta').modal('show');
    }); 

    $('#myModalplanta').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });


});