var tblConvenioPta;
var modal_title;
var cliente = null;
var enviando = false;
var boton_editar_elim = document.getElementById("botonconvjs");
var boton_guardarconv = document.getElementById("botonConv");
boton_editar_elim.addEventListener("click", guardar_convenio);
boton_guardarconv.addEventListener("click", guardar_convenio);

function getData5() {
    tblConvenioPta = $('#data-table-fixed-header').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/clientes/'+cliente+'/planta_convenios/',
            type: 'POST',
            data: {
                'action': 'searchdata5'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "nombre"},
            {"data": "valor"},
            {"data": "validez"},
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

    getData5();


    $('#data-table-fixed-header tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Convenio Planta <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblConvenioPta.cell($(this).closest('td, li')).index();
        var data = tblConvenioPta.row(tr.row).data();
        $('input[name="action"]').val('convenio_edit');
        $('input[name="id"]' ).val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="valor"]').val(data.valor);
        $('input[name="validez"]').val(data.validez);

        var insumo2 = [];
        data.insumo.forEach(function(insumos, index) { 
            var insumo1 = insumos.id;
            insumo2 = insumo2.concat(insumo1);
            });

        $('select[name="insumo"]').val(insumo2).trigger("change");

        $('input[name="cliente_id"]').val(data.cliente_id);
        $('input[name="planta_id"]').val(data.planta_id);
        var btn = document.getElementById("botonconvjs");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalConvenioPlanta').modal('show');
    });

    $('#data-table-fixed-header tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Convenio Planta <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblConvenioPta.cell($(this).closest('td, li')).index();
        var data = tblConvenioPta.row(tr.row).data();
        $('input[name="action"]').val('convenio_delete');
        $('input[name="id"]' ).val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="valor"]').val(data.valor);
        $('input[name="validez"]').val(data.validez);

        var insumo2 = [];
        data.insumo.forEach(function(insumos, index) { 
            var insumo1 = insumos.id;
            insumo2 = insumo2.concat(insumo1);
            });

        $('select[name="insumo"]').val(insumo2).trigger("change");

        var btn = document.getElementById("botonconvjs");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalConvenioPlanta').modal('show');
    });

    $('#myModalConvenioPlanta').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('.btnAdd3').on('click', function () {

        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            // console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalConvenioPlanta').modal('hide');
                $('#myModalConvenio').modal('hide');
                tblConvenioPta.ajax.reload();
            }); 
        });

    });
});

function guardar_convenio() { 
    if (enviando == false){
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            // console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalConvenioPlanta').modal('hide');
                $('#myModalConvenio').modal('hide');
                tblConvenioPta.ajax.reload();
            });
            enviando = True;   
        });  
    }
  }