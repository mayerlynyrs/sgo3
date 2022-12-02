var tblPlanta;
var modal_title;
var cliente = null;
var enviando = false;
var boton_numero2 = document.getElementById("boton2");
boton_numero2.addEventListener("click", guardar_planta);


function getData3() {
    tblPlanta = $('#data-table-buttons_wrapper').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/clientes/'+cliente+'/plantas/',
            type: 'POST',
            data: {
                'action': 'searchdata3'
            },
            dataSrc: ""
        },

        columns: [
            {"data": "nombre",
            "render": function(data, type, meta){
                data = ''+ data;
                return data;
            }},
            {"data": "rut"},
            {"data": "negocio"},
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
                    buttons += '<a href="'+data+'" data-toggle="modal" data-target="#myModalContactoPlanta" rel="agg" title="Agregar Contactos" class="btn btn-primary btn-xs btn-flat btnAgg"><i class="fas fa-users"></i></a> &nbsp &nbsp &nbsp &nbsp';
                    buttons += '<a href="'+data+'" data-toggle="modal" data-target="#myModalConvenio" rel="agregar" title="Agregar Convenio" class="btn btn-dark btn-xs btn-flat btnAgg"><i class="fas fa-box-open"></i></a>';
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

    getData3();

    jQuery('#fecha').datetimepicker({
        timepicker : false,
        format:'Y-m-d',
      });

    $('.btnAddplanta').on('click', function () {
        $('input[name="action"]').val('planta_add');
        modal_title.find('span').html('Planta <small style="font-size: 80%;">Nuevo</small>');
        console.log(modal_title.find('i'));
        $('form')[2].reset();
        modal_title.find('i').removeClass().addClass();
        $('form')[2].reset();
        var btn = document.getElementById("boton2");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Guardar';
        $('#myModalPlanta').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Planta <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblPlanta.cell($(this).closest('td, li')).index();
        var data = tblPlanta.row(tr.row).data();
        $('input[name="action"]').val('planta_edit');
        $('input[name="id"]' ).val(data.id);
        $('select[name="negocio"]').val(data.negocio_id).trigger("change");
        $('input[name="rut"]').val(data.rut);
        $('input[name="cod_uny_planta"]').val(data.codigo);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="telefono"]').val(data.telefono);
        $('input[name="email"]').val(data.email);
        $('select[name="region2"]').val(data.region_id).trigger("change");
        $('select[name="provincia2"]').val(data.provincia_id).trigger("change");
        $('select[name="ciudad2"]').val(data.ciudad_id).trigger("change");
        $('input[name="direccion"]').val(data.direccion);
        $('input:checkbox[name=masso]').attr('checked',data.masso);
        $('input:checkbox[name=hal2]').attr('checked',data.hal2);
        $('input:checkbox[name=psicologico]').attr('checked',data.psicologico);     
        var bono2 = [];
        data.bono.forEach(function(bonos, index) { 
            var bonos1 = bonos.id;
            bono2 = bono2.concat(bonos1);
            });
            
        $('select[name="bono"]').val(bono2).trigger("change");
        $('select[name="gratificacion"]').val(data.gratificacion).trigger("change");
        $('select[name="bateria"]').val(data.bateria).trigger("change");
        $('input[name="rut_gerente"]').val(data.rut_gerente);
        $('input[name="nombre_gerente"]').val(data.nombre_gerente);
        $('input[name="direccion_gerente"]').val(data.direccion_gerente);
        var btn = document.getElementById("boton2");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalPlanta').modal('show');
        return data;
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Planta <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblPlanta.cell($(this).closest('td, li')).index();
        var data = tblPlanta.row(tr.row).data();
        $('input[name="action"]').val('planta_delete');
        $('input[name="id"]' ).val(data.id);
        $('select[name="negocio"]').val(data.negocio_id).trigger("change");
        $('input[name="rut"]').val(data.rut);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="telefono"]').val(data.telefono);
        $('input[name="cod_uny_planta"]').val(data.codigo);
        $('input[name="email"]').val(data.email);
        $('select[name="region2"]').val(data.region_id).trigger("change");
        $('select[name="provincia2"]').val(data.provincia_id).trigger("change");
        $('select[name="ciudad2"]').val(data.ciudad_id).trigger("change");
        $('input[name="direccion"]').val(data.direccion);
        $('input:checkbox[name=masso]').attr('checked',data.masso);
        $('input:checkbox[name=hal2]').attr('checked',data.hal2);
        $('input:checkbox[name=psicologico]').attr('checked',data.psicologico);   
        var bono2 = [];
        data.bono.forEach(function(bonos, index) { 
            var bonos1 = bonos.id;
            bono2 = bono2.concat(bonos1);
            });
            
        $('select[name="bono"]').val(bono2).trigger("change");
        $('select[name="gratificacion"]').val(data.gratificacion).trigger("change");
        $('select[name="bateria"]').val(data.bateria).trigger("change");
        $('input[name="rut_gerente"]').val(data.rut_gerente);
        $('input[name="nombre_gerente"]').val(data.nombre_gerente);
        $('input[name="direcccion_gerente"]').val(data.direcccion_gerente);
        var btn = document.getElementById("boton2");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalPlanta').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="agg"]', function (){
        $('input[name="action"]').val('cp_contacto_add');
        modal_title.find('span').html('Contacto Planta(es) <small style="font-size: 80%;">Nuevo</small>' );
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        var tr = tblPlanta.cell($(this).closest('td, li')).index();
        var data = tblPlanta.row(tr.row).data();
        $('form')[3].reset();
        $('input[name="planta_id"]').val(data.id);
        console.log(data.id);
       
        $('#myModalContactoPlanta').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="agregar"]', function (){
        $('input[name="action"]').val('convenio_add');
        modal_title.find('span').html('Convenio Planta(s) <small style="font-size: 80%;">Nuevo</small>' );
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        var tr = tblPlanta.cell($(this).closest('td, li')).index();
        var data = tblPlanta.row(tr.row).data();
        $('form')[4].reset();
        $('input[name="planta_id"]').val(data.id);
        console.log(data.id);
       
        $('#myModalConvenio').modal('show');
    });


    $('#myModalPlanta').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });


});

function guardar_planta() { 
    if (enviando == false){
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalPlanta').modal('hide');
                tblPlanta.ajax.reload();
                $('#myModalPlanta')[0].reset();
            });
            enviando = True;   
        });  
    }
  }