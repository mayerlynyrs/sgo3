var tblSolicitud;
var modal_title;

function getData() {
    tblSolicitud = $('#data-table-default').DataTable({
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
            {"data": "id",
            "class": 'text-center',
            "render": function(data, type, row, meta){
                data = '<input  data-id="'+data+'" class="form-check-input" value="'+data+'" name="check_aprobacion" type="checkbox" title="Ver Contrato" ></input>';
                return data;
            }},
            
            {"data": "trabajador"},
            {"data": "requerimiento"},
            {"data": "plazos"},
            {"data": "contrato"},
            {"data": "estado_firma",
            "class": 'text-center d-none',
            "render": function(data, type, row, meta){
                data = '<input hidden data-id="'+data+'" value="'+data+'" name="estado" id="estado" ></input>';
                return data;
            }},
            {"data": "id"},
            
   
        ],

        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#"  rel="aprobar" title="Enviar a Firma" class="btn btn-outline-success btn-xs btn-flat btnEdit"><i class="fa fa-signature"></i></a> &nbsp &nbsp &nbsp &nbsp';
                    // buttons += '<a href="#"  rel="rechazar" title="'+data+'" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-window-close"></i></a> &nbsp &nbsp &nbsp &nbsp';
                    buttons += '<button   data-id="'+data+'" name="estado" value="'+data+'" onclick="myFunction('+data+')"  id="btn-view-contrato" type="button" title="Ver Contrato" class="btn btn-xs btn-outline-primary"><i class="fas fa-eye"></i></button>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

function myFunction(data) {
      var id = data;
      var URL = '/contratos/'+id+'/solicitudes-pendientes/';
      $.ajax({
            url: URL,
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
              $("#modal-contrato").modal("show");
            },
            success: function (data) {
                $("#modal-contrato .modal-content").html(data.html_form);
            }
          });
  }

$(function () {

    modal_title = $('.modal-title');

    getData();


    $('#data-table-default tbody').on('click', 'a[rel="aprobar"]', function (){
        var tr = tblSolicitud.cell($(this).closest('td, li')).index();
        var data = tblSolicitud.row(tr.row).data();
        modal_title.find('span').html('Enviar Anexo a <small style="font-size: 80%;">'+data.nombre+'</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        $('input[name="action"]').val('aprobar');
        $('input[name="id"]' ).val(data.id);
        document.getElementById('observacion').style.display = 'none';
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#32a932';
        btn.style.backgroundColor= '#32a932';
        btn.innerHTML = 'Enviar';
        $('#solicitudes_contrato').modal('show');

    });

    $('#data-table-default tbody').on('click', 'a[rel="rechazar"]', function (){
        var tr = tblSolicitud.cell($(this).closest('td, li')).index();
        var data = tblSolicitud.row(tr.row).data();
        modal_title.find('span').html('Rechazar Contrato <small style="font-size: 80%;">'+data.nombre+'</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        $('input[name="action"]').val('rechazar');
        $('input[name="id"]' ).val(data.id);
        document.getElementById('observacion').style.display = 'block';
        var btn = document.getElementById("boton");
        btn.style.borderColor= '#ff5b57';
        btn.style.backgroundColor= '#ff5b57';
        btn.innerHTML = 'Rechazar';
        $('#solicitudes_contrato').modal('show');
    });

    $('#solicitudes_contrato').on('shown.bs.modal', function () {
    });

    $("#myform").on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        console.log(FormData);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#solicitudes_contrato').modal('hide');
            tblSolicitud.ajax.reload();
        });   
    });
});