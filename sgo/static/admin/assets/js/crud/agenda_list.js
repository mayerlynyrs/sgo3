var tblAgenda;
var modal_title;


function getData() {
    tblAgenda = $('#data-table-default').DataTable({
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
            {"data": "user"},
            {"data": "fecha_agenda_evaluacion"},
            {"data": "fecha_ingreso_estimada"},
            {"data": "psicologo"},
            {"data": "id"},
        ],
        buttons: [{
            extend: 'excelHtml5',
            text: 'hola',
            titleAttr: 'Exportar a Excel',
            className: 'btn btn-success'

        }],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a>  &nbsp &nbsp';
                    buttons += '<a href="#" rel="delete" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> &nbsp &nbsp';
                    buttons += '<a href="#" data-toggle="modal" data-target="#myModalEvaluacion" rel="agg" title="Evaluar" class="btn btn-primary btn-xs btn-flat btnAgg"><i class="fas fa-fw fa-newspaper"></i></a>';
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
        modal_title.find('span').html('Sistema de Previsión <small style="font-size: 80%;">Nuevo</small>');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[0].reset();
        var btn = document.getElementById("btn-guardar");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('#myModalAgenda').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="edit"]', function (){
    
        
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblAgenda.cell($(this).closest('td, li')).index();
        var data = tblAgenda.row(tr.row).data();
        modal_title.find('span').html('Agendar a ' +data.user+ '<small style="font-size: 90%;"> <br> Nombre: '+data.user+
        ' &nbsp &nbsp RUT '+data.user_rut +'&nbsp &nbsp Comuna: '+data.user_ciudad +'<br> Telefono: '+data.user_telefono+' &nbsp &nbsp Correo: '+data.user_email +' </small>');
        $('input[name="rut"]' ).val(data.rut);
        $('input[name="action"]').val('edit');
        $('input[name="id"]' ).val(data.id);
        $('select[name="estado"]').val(data.estado).trigger("change");
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('input[name="fecha_ingreso_estimada"]').val(data.fecha_ingreso_estimada);
        $('input[name="fecha_agenda_evaluacion"]').val(data.fecha_agenda_evaluacion);
        $('select[name="planta"]').val(data.planta).trigger("change");
        $('select[name="cargo"]').val(data.cargo).trigger("change");
        $('select[name="evaluacion"]').val(data.evaluacion).trigger("change");
        $('select[name="psico"]').val(data.psico).trigger("change");
        $('input:checkbox[name=Hal2]').attr('checked',data.Hal2);  
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('textarea[name="obs"]').val(data.obs);
        var btn = document.getElementById("btn-guardar");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalAgenda').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Sistema de Previsión <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblAgenda.cell($(this).closest('td, li')).index();
        var data = tblAgenda.row(tr.row).data();
        $('input[name="action"]').val('delete');
        $('input[name="id"]' ).val(data.id);
        $('select[name="estado"]').val(data.estado).trigger("change");
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('input[name="fecha_ingreso_estimada"]').val(data.fecha_ingreso_estimada);
        $('input[name="fecha_agenda_evaluacion"]').val(data.fecha_agenda_evaluacion);
        $('select[name="planta"]').val(data.planta).trigger("change");
        $('select[name="evaluacion"]').val(data.evaluacion).trigger("change");
        $('input:checkbox[name=Hal2]').attr('checked',data.Hal2);  
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('textarea[name="obs"]').val(data.obs);
        var btn = document.getElementById("btn-guardar");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalAgenda').modal('show');
    });

    $('#data-table-default tbody').on('click', 'a[rel="agg"]', function (){
        $('input[name="action"]').val('evaluacion_add');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        var tr = tblAgenda.cell($(this).closest('td, li')).index();
        var data = tblAgenda.row(tr.row).data();   
        modal_title.find('span').html('Evaluar <small style="font-size: 90%;"> <br> Nombre: '+data.user+
        ' &nbsp &nbsp RUT '+data.user_rut +'&nbsp &nbsp Comuna: '+data.user_ciudad +'<br> Telefono: '+data.user_telefono+' &nbsp &nbsp Correo: '+data.user_email +' </small>');
        $('form')[0].reset();
        $('input[name="id"]' ).val(data.id);
        $('input[name="user_id"]').val(data.user_id);
        $('select[name="planta"]').val(data.planta).trigger("change");
        $('select[name="cargo"]').val(data.cargo).trigger("change");
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('input[name="psicologo"]').val(data.psico);
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        
       
        $('#myModalEvaluacion').modal('show');
    });

    $('#myModalAgenda').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        console.log(FormData);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalAgenda').modal('hide');
            $('#myModalEvaluacion').modal('hide');
            tblAgenda.ajax.reload();
        });   
    });
});