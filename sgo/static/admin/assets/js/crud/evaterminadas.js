var tblnegocio;
var modal_title;
var cliente = null;

function getData() {
    tblnegocio = $('#data-table-default').DataTable({
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
            {
            "data": "nombre"
            },
            {"data": "descripcion"},
            {"data": "archivo",
            "render": function(data, type, row, meta){
                data = '<a href="/../../media/' + data + '">' + ' <i class="fa fa-download" aria-hidden="true"></i></a> ';
                // data = '<a href="/../../media/' + data + '">' + ' <button data-id="1" type="button" class="btn btn-xs btn-success btn-view-fichero"><i class="fas fa-eye"></i> Visualizar</button></a> ';
                return data;
            }},
            {"data": "id"},
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    getData();


});