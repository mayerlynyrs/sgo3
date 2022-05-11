var tblListNegra;
var modal_title;

function getData() {
    tblListNegra = $('#data-table-default').DataTable({
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
            {"data": "trabajador"},
            {"data": "descripcion"},
            {"data": "tipo"},
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

    getData();

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Lista Negra' );
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[0].reset();
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar'
        $('#ModalListaNegra').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Edición de una Lista Negra');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblListNegra.cell($(this).closest('td, li')).index();
        var data = tblListNegra.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]' ).val(data.id);
        $('select[name="trabajador"]').val(data.trabajador_id).trigger("change");
        $('textarea[name="descripcion"]').val(data.descripcion);
        $('input[name="tipo"]').val(data.tipo);
        $('select[name="planta"]').val(data.planta_id).trigger("change");
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#ModalListaNegra').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('¿Desea Eliminar de la Lista Negra?');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblListNegra.cell($(this).closest('td, li')).index();
        var data = tblListNegra.row(tr.row).data();
        $('input[name="action"]').val('delete');
        $('input[name="id"]').val(data.id);
        $('select[name="trabajador"]').val(data.trabajador_id).trigger("change");
        $('textarea[name="descripcion"]').val(data.descripcion);
        $('input[name="tipo"]').val(data.tipo);
        $('select[name="planta"]').val(data.planta_id).trigger("change");
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#ModalListaNegra').modal('show');
    }); 

    $('#ModalListaNegra').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        console.log(FormData);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#ModalListaNegra').modal('hide');
            tblListNegra.ajax.reload();
        });   
    });
});