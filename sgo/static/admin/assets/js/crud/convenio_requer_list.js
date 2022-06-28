var tblConvenioReq;
var modal_title;
var requerimiento = null;
var enviando = false;
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
    requerimiento = document.getElementById("requerimiento_id").value;

    getData3();

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

    $('#myModalConvenioR').on('shown.bs.modal', function () {
        // $('form')[0].reset();
    });

});

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
