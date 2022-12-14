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
            // {"data": "id",
            // "class": 'text-center',
            // "render": function(data, type, row, meta){
            //     data = '<input  data-id="'+data+'" class="form-check-input" value="'+data+'" name="check_aprobacion" type="checkbox" title="Seleccionar" ></input>';
            //     return data;
            // }},
            
            {"data": "trabajador"},
            {"data": "requerimiento"},
            {"data": "plazos"},
            {"data": "contrato"},
            {"data": "estados"},
            {"data": "id"},
            
   
        ],

        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<button data-id="'+data+'" name="estado" value="'+data+'" onclick="myFunction('+data+')"  id="btn-view-contrato" type="button" title="Ver estado" class="btn btn-xs btn-outline-primary"><i class="fas fa-folder-open"></i></button> &nbsp &nbsp';
                    // buttons += '<a href="#" rel="aprobar" title="Enviar a Firma" class="btn btn-outline-success btn-xs btn-flat btnEdit"><i class="fa fa-signature"></i></a> &nbsp &nbsp';
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
      var URL = '/firmas/'+id+'/estado/';
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
        modal_title.find('span').html('Enviar Contrato a <small style="font-size: 80%;">'+data.nombre+'</small>');
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