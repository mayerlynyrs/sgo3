var tblConvenioReq;
var tblConveniosReq;
var modal_title;
var requerimiento = null;
var enviando = false;
var accion = 0;
var trabajador = 0;
var boton_convenio = document.getElementById("botonConvenio");
boton_convenio.addEventListener("click", guardar_convenio);


function getData3() {
    tblConvenioReq = $('#data-table-responsive').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/requerimientos/'+requerimiento+'/convenios/',
            type: 'POST',
            data: {
                'action': 'searchdata3'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "convenio"},
            {"data": "convenio_insumo[ <br> ].nombre"},
            {"data": "area_cargo"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> &nbsp &nbsp &nbsp &nbsp';
                    buttons += '<a href="#" rel="delete" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> &nbsp &nbsp &nbsp &nbsp';
                    // buttons += '<a href="#" rel="agg" title="Asignar EPP" data-target="#myModalAddEpp" class="btn btn-info btn-xs btn-flat btnEdit"><i class="fas fa-clipboard-check"></i></a>';
                    buttons += '<a href="'+data+'" data-toggle="modal" data-target="#myModalAddEpp" rel="agg" title="Asignar EPP" class="btn btn-info btn-xs btn-flat btnAgg"><i class="fas fa-clipboard-check"></i></a>';
                    // buttons += '<a href="#" data-toggle="modal" data-target="#myModalRequerTrab" rel="agg" title="Agregar Trabajador(es)" class="btn btn-primary btn-xs btn-flat btnAgg"><i class="fas fa-users"></i></a>';
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
    modal_body2 = $('.modal-body2');
    requerimiento = document.getElementById("requerimiento_id").value;

    getData3();
    

    function getData6(a_c) {
        tblConveniosReq = $('#data-table-fixed-cabo').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: '/requerimientos/'+a_c+'/convenios_trabajadores/',
                type: 'POST',
                data: {
                    'action': 'searchdata6'
                },
                dataSrc: ""
            },
            columns: [
                {"data": "datos"},
                {"data": "trabajador_id"},
                
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        // var buttons = '<button onclick="miFunc()">Haz click</button> &nbsp &nbsp &nbsp &nbsp';
                        var buttons = '<button onclick="miFunc(accion=1, '+data+')" rel="yes" title="Confirmar" class="btn btn-lime btn-xs btn-flat"><i class="fas fa-check"></i></button> &nbsp &nbsp &nbsp &nbsp';
                        buttons += '<button onclick="miFunc(accion=2, '+data+')" rel="not" title="Anular" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-times"></i></button> &nbsp &nbsp &nbsp &nbsp';
                        // buttons += '<a href="create_requerimiento" rel="not" title="Anular" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-times"></i></a> &nbsp &nbsp &nbsp &nbsp';
                        // buttons += '<a href="'+data+'" rel="not" title="Anular" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-times"></i></a> &nbsp &nbsp &nbsp &nbsp';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
    
            }
        });
    }


    $('.btnAddConvenio').on('click', function () {
        $('input[name="action"]').val('convenio_add');
        modal_title.find('span').html('<b style="font-size: 1.25rem;">Convenio del Requerimiento </b><small style="font-size: 80%;">Nuevo</small>');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[2].reset();
        var btn = document.getElementById("botonConvenio");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('#myModalConvenioR').modal('show');
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('<b style="font-size: 1.25rem;">Convenio del Requerimiento </b><small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblConvenioReq.cell($(this).closest('td, li')).index();
        var data = tblConvenioReq.row(tr.row).data();
        $('input[name="action"]').val('convenio_edit');
        $('input[name="id"]' ).val(data.id);
        $('select[name="convenio"]').val(data.convenio_id).trigger("change");
        $('select[name="area_cargo"]').val(data.area_cargo_id).trigger("change");
        var btn = document.getElementById("botonConvenio");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalConvenioR').modal('show');
        console.log(data);
        return data;
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('<b style="font-size: 1.25rem;">Convenio del Requerimiento </b><small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblConvenioReq.cell($(this).closest('td, li')).index();
        var data = tblConvenioReq.row(tr.row).data();
        $('input[name="action"]').val('convenio_delete');
        $('input[name="id"]').val(data.id);
        $('select[name="convenio"]').val(data.convenio_id).trigger("change");
        $('select[name="area_cargo"]').val(data.area_cargo_id).trigger("change");
        var btn = document.getElementById("botonConvenio");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalConvenioR').modal('show');
    });

    $('#data-table-responsive tbody').on('click', 'a[rel="agg"]', function (){
        modal_title.find('span').html('<b style="font-size: 1.25rem;">Asignar EPP </b><small style="font-size: 80%;">Nuevo</small>' );
        // console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        var tr = tblConvenioReq.cell($(this).closest('td, li')).index();
        var data = tblConvenioReq.row(tr.row).data();
        a_c = data.area_cargo_id;
        getData6(a_c);
        $('form')[3].reset();
        insumos = [];
        data.convenio_insumo.forEach(function(elemento, indice, array) {
            insumos.push(elemento.nombre);
        });

        modal_body2.find('span').html('<small style="font-size: 90%; line-height: 250%">' +
        '<b style="color: #242a30; font-weight: 600;">Área-Cargo:</b> ' + 
        data.a_c +'<br> <b style="color: #242a30; font-weight: 600;">Convenio:</b> ' +
        data.convenio + '<br> <b style="color: #242a30; font-weight: 600;">Insumo(s):</b> ' +
        insumos + ' <br><br></small>');
        modal_body2.find('i').removeClass().addClass();
        $('input[name="convenio_id"]').val(data.convenio_id);
        $('input[name="area_cargo_id"]').val(data.area_cargo_id);
        $('input[name="trabajador_id"]').val(data);
        $('input[name="insumos"]').val(data.convenio_insumo.forEach(function(elemento, indice, array) { elemento.nombre; }));
        console.log(data.id);
        $('#myModalAddEpp').modal('show');
    });

    $('#myModalConvenioR').on('shown.bs.modal', function () {
        // $('form')[0].reset();
    });

});
  function miFunc(accion, data) {
    $('input[name="action"]').val(accion);
    $('input[name="trabajador_id"]').val(data);
    if (accion == 1){
        iziToast.success({
            position: 'topRight',
            message: 'Tabajador Confirmado'
        });
    } else {
        iziToast.error({
            position: 'topRight',
            message: 'Tabajador Anulado'
        });
    }
    if (enviando == false){
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                // $('#myModalAddEpp').modal('hide');
                tblConvenioReq.ajax.reload();
                tblConveniosReq.ajax.reload();
            });
            enviando = True;   
        });  
    }
  }

function guardar_convenio() { 
    if (enviando == false){
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalConvenioR').modal('hide');
                tblConvenioReq.ajax.reload();
            });
            enviando = True;   
        });  
    }
  }
