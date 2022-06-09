var tblProfesionTrab;
var modal_title;
var trabajador_id = null;
var enviando = false;
var boton_numero2 = document.getElementById("boton1");
boton_numero2.addEventListener("click", guardar_profesion);  


function getData2() {
    tblProfesionTrab = $('#data-table-buttons_wrapper').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/users/'+trabajador_id+'/profesion_trabajadores/',
            type: 'POST',
            data: {
                'action': 'searchdata3'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "egreso"},
            {"data": "institucion"},
            {"data": "profesion"},
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

    $('#egreso').datepicker({
        format: "yyyy-mm-dd",
        language: 'es'
    });
    
    modal_title = $('.modal-title');
    trabajador_id = document.getElementById("trabajador_id").value;

    getData2();

    $('.btnAddProfes').on('click', function () {
        $('input[name="action"]').val('profesion_add');
        modal_title.find('span').html('Profesión <small style="font-size: 80%;">Nuevo</small>' );
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[2].reset();
        var btn = document.getElementById("boton1");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('#myModalProfesionTrab').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Profesión <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblProfesionTrab.cell($(this).closest('td, li')).index();
        var data = tblProfesionTrab.row(tr.row).data();
        $('form')[2].reset();
        $('input[name="action"]').val('profesion_edit');
        $('input[name="id"]' ).val(data.id);
        $('input[name="egreso"]').val(data.egreso);
        $('input[name="institucion"]').val(data.institucion);
        $('select[name="profesion"]').val(data.profesion_id).trigger("change");
        var btn = document.getElementById("boton1");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalProfesionTrab').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Profesión <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblProfesionTrab.cell($(this).closest('td, li')).index();
        var data = tblProfesionTrab.row(tr.row).data();
        $('input[name="action"]').val('profesion_delete');
        $('input[name="id"]').val(data.id);
        $('input[name="egreso"]').val(data.egreso);
        $('input[name="institucion"]').val(data.institucion);
        $('select[name="profesion"]').val(data.profesion_id).trigger("change");
        var btn = document.getElementById("boton1");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar'
        $('#myModalProfesionTrab').modal('show');
    }); 

    $('#myModalProfesionTrab').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

});

function guardar_profesion() { 
    if (enviando == false){ 
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalProfesionTrab').modal('hide');
                tblProfesionTrab.ajax.reload();
            });
            enviando = True; 
        });
    }
  }