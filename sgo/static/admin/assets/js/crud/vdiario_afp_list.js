var tblValorDiario;
var modal_title;

function getData() {
    tblValorDiario = $('#data-table-default').DataTable({
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
            {"data": "valor"},
            {"data": "afp"},
            {"data": "valor_diario"},
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

    getData();

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Valor Diario AFP<small style="font-size: 80%;">Nuevo</small>');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[0].reset();
        $('#myModalValorDiarioAfp').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Valor Diario AFP<small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblValorDiario.cell($(this).closest('td, li')).index();
        var data = tblValorDiario.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]' ).val(data.id);
        $('input[name="valor_diario"]').val(data.valor_diario);
        $('#myModalValorDiarioAfp').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Valor Diario AFP<small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblValorDiario.cell($(this).closest('td, li')).index();
        var data = tblValorDiario.row(tr.row).data();
        $('input[name="action"]').val('delete');
        $('input[name="id"]').val(data.id);
        $('input[name="valor_diario"]').val(data.valor_diario);
        $('#myModalValorDiarioAfp').modal('show');
    });

    $('#myModalValorDiarioAfp').on('shown.bs.modal', function () {

    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        console.log(FormData);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalValorDiarioAfp').modal('hide');
            tblValorDiario.ajax.reload();
        });   
    });
});