var tblRequeriTrab;
var tblAsignarTrab;
var modal_title;
var requerimiento = null;
var enviando = false;
var accion = 0;
var id = 0;
var trabajador= 0;
var boton_numero2 = document.getElementById("boton2");
boton_numero2.addEventListener("click", guardar_planta_contacto);
var boton_rev_exam = document.getElementById("botonRevExam");
boton_rev_exam.addEventListener("click", guardar_rev_exam);
var boton_asignar = document.getElementById("btnAsignar");
boton_asignar.addEventListener("click", guardar_asignacion);


function getData4() {
    tblRequeriTrab = $('#data-table-buttons_wrapper').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: '/requerimientos/'+requerimiento+'/requirement_trabajadores/',
            type: 'POST',
            data: {
                'action': 'searchdata4'
            },
            dataSrc: ""
        },
        columns: [
            // {"data": "id",
            // "render": function(data, type, row, meta){
            //     data = '<a href="../../../contratos/'+data+'/create_contrato/ " class="btn btn-primary btn-xs"><i class="fas fa-file" title="Solicitud de Contrato" aria-hidden="true"></i></a> ';
            //     return data;
            // }},
            {"data": "area_cargo"},
            {"data": "trabajador"},
            {"data": "jefe_area"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> &nbsp &nbsp';
                    buttons += '<a href="#" rel="delete" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> &nbsp &nbsp';
                    buttons += '<a href="'+data+'" data-toggle="modal" data-target="#myModalAsignar" rel="allow" title="Asignar EPP" class="btn btn-info btn-xs btn-flat btnAgg"><i class="fas fa-clipboard-check"></i></a> &nbsp &nbsp';
                    // buttons += '<a href="'+data+'" data-toggle="modal" data-target="#myModalAsignar" rel="agg" title="Asignar EPP" class="btn btn-info btn-xs btn-flat btnAgg"><i class="fas fa-clipboard-check"></i></a>';
                    // buttons += '<a href="'+data+'" data-toggle="modal" data-target="#myModalAddEpp" rel="agg" title="Asignar EPP" class="btn btn-info btn-xs btn-flat btnAgg"><i class="fas fa-clipboard-check"></i></a>';
                    // buttons += '<a href="#" rel="edit" title="Asignar EPP" class="btn btn-dark btn-xs btn-flat btnEdit"><i class="fas fa-clipboard-check"></i></a> &nbsp &nbsp';
                    // buttons += '<a href="#" rel="validation" title="Validación" class="btn btn-green btn-xs btn-flat btnAgg"><i class="fas fa-check-double"></i></a> &nbsp &nbsp';
                    buttons += '<a href="../../../contratos/'+data+'/create_contrato/" rel="request" title="Solicitud de Contrato" class="btn btn-success btn-xs btn-flat btnAgg4"><i class="fas fa-file"></i></a> &nbsp &nbsp';
                    // buttons += '<a href="#" rel="status" title="Estado de solicitud" class="btn btn-info btn-xs btn-flat btnAgg"><i class="fas fa-square"></i></a> &nbsp &nbsp';
                    // buttons += '<a href="#" rel="record" title="Historial" class="btn btn-secondary btn-xs btn-flat btnAgg"><i class="fas fa-list"></i></a>';
                    // data-toggle="modal" data-target="#myModalRequerTrab" 
                    // buttons += '<a href="#" rel="edit" title="Enviar a Revisión" class="btn btn-primary btn-xs btn-flat btnEdit"><i class="fas fa-hospital"></i></a>';
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
    requerimiento = document.getElementById("requerimiento_id").value;

    getData4();
    

    function getData8(trabajador_id) {
        tblAsignarTrab = $('#data-table-fixed-spa').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: '/requerimientos/'+trabajador_id+'/asignar_trabajador/',
                type: 'POST',
                data: {
                    'action': 'searchdata8'
                },
                dataSrc: ""
            },
            columns: [
                {"data": "insumo"},
                {"data": "cantidad"},
                {"data": "id"},
                
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        // var buttons = '<button onclick="miFuncDelete(accion=3, '+data+')" rel="not" title="Anular'+data+'" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-times"></i></button> &nbsp &nbsp &nbsp &nbsp';
                        var buttons = '<button onclick="miFuncDelete(accion=3, '+data+')" rel="not" title="Anular'+data+'" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-times"></i></button> &nbsp &nbsp &nbsp &nbsp';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
    
            }
        });
    }

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="edit"]', function (){
    
        modal_title.find('span').html('Trabajador(es) <small style="font-size: 80%;">Editar</small>');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblRequeriTrab.cell($(this).closest('td, li')).index();
        var data = tblRequeriTrab.row(tr.row).data();
        $('input[name="action"]').val('requeri_trab_edit');
        $('input[name="id"]' ).val(data.id);
        $('select[name="area_cargo"]').val(data.area_cargo_id).trigger("change");
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('select[name="trabajador"]').val(data.trabajador_id).trigger("change");
        $('input[name="pension"]').val(data.pension);
        $('select[name="jefe_area"]').val(data.jefe_area_id).trigger("change");
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('textarea[name="descripcion"]').val(data.descripcion);
        var btn = document.getElementById("boton3");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Editar';
        $('#myModalRequerUser').modal('show');
    });

    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="delete"]', function (){
    
        modal_title.find('span').html('Trabajador(es) <small style="font-size: 80%;">Eliminar</small>');
        modal_title.find('i').removeClass().addClass('fa fa-trash');
        var tr = tblRequeriTrab.cell($(this).closest('td, li')).index();
        var data = tblRequeriTrab.row(tr.row).data();
        $('input[name="action"]').val('requeri_trab_delete');
        $('input[name="id"]').val(data.id);
        $('select[name="area_cargo"]').val(data.area_cargo_id).trigger("change");
        $('input:checkbox[name=referido]').attr('checked',data.referido);
        $('textarea[name="descripcion"]').val(data.descripcion);
        $('select[name="tipo"]').val(data.tipo).trigger("change");
        $('input[name="pension"]').val(data.pension);
        $('select[name="trabajador"]').val(data.trabajador_id).trigger("change");
        $('select[name="jefe_area"]').val(data.jefe_area_id).trigger("change");
        var btn = document.getElementById("boton3");
        btn.style.borderColor= '#de555e';
        btn.style.backgroundColor= '#de555e';
        btn.innerHTML = 'Eliminar';
        $('#myModalRequerUser').modal('show');
    });


    $('.btnSendExam').on('click', function () {
        $('input[name="action"]').val('exam_rev_add');
        modal_title.find('span').html('<b style="font-size: 1.25rem;">Revisión de Exámenes </b><small style="font-size: 80%;">Enviar</small>');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        $('form')[2].reset();
        var btn = document.getElementById("botonRevExam");
        btn.style.borderColor= '#153264';
        btn.style.backgroundColor= '#153264';
        btn.innerHTML = 'Si';
        $('#myModalSendExam').modal('show');
    });


    $('#data-table-buttons_wrapper tbody').on('click', 'a[rel="allow"]', function (){
        // console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass();
        var tr = tblRequeriTrab.cell($(this).closest('td, li')).index();
        var data = tblRequeriTrab.row(tr.row).data();
        trabajador_id = data.trabajador_id;
        a_c = data.area_cargo_id;
        getData8(trabajador_id);
        modal_title.find('span').html('<b style="font-size: 1.25rem;">Asignar Epps </b><small style="font-size: 80%;">' + data.trabajador + '</small>' );
        $('form')[3].reset();
        $('input[name="area_cargo_id"]').val(data.area_cargo_id);
        $('input[name="requerimiento_id"]').val(data.requerimiento_id);
        $('input[name="trabajador_id"]').val(data.trabajador_id);
        $('input[name="trabajador"]').val(data.trabajador);
        $('input[name="action"]').val('epp_trab_add');
        $('input[name="id"]').val(0);
        // console.log(data.id);
        $('#myModalAsignar').modal('show');
    });



    $('#myModalRequerUser').on('shown.bs.modal', function () {
        $('form')[0].reset();
    });

    $('.btnAdd3').on('click', function () {

        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalACR').modal('hide');
                tblAreaCargo.ajax.reload();
                $('#myModalRequerTrab').modal('hide');
                $('#myModalRequerUser').modal('hide');
                tblRequeriTrab.ajax.reload();
            }); 
        });

    });
});

function guardar_planta_contacto() { 
    if (enviando == false){
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalRequerTrab').modal('hide');
                $('#myModalRequerUser').modal('hide');
                tblRequeriTrab.ajax.reload();
                tblAsignarTrab.ajax.reload();
            });
            enviando = True;   
        });  
    }
  }

function guardar_rev_exam() { 
    if (enviando == false){
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalSendExam').modal('hide');
                iziToast.success({
                    position: 'topRight',
                    message: 'Enviado(s) a Revisión'
                })
            });
            enviando = True;   
        });  
    }
  }

  function guardar_asignacion() { 
      if (enviando == false){
          $('#EppAsignar').on('submit', function (e) {
              e.preventDefault();
              var parameters = new FormData(this);
              console.log(FormData);
              submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                  $("#myModalAsignar").find("input,textarea").val("");
                  $("#myModalAsignar").find("select").val("").trigger("change");
                  $("#myModalAsignar input[type='checkbox']").prop('checked', false).change()
                  $('#myModalAsignar').modal('hide');
                  tblRequeriTrab.ajax.reload();
                  tblAsignarTrab.ajax.reload();
                  iziToast.success({
                      position: 'topRight',
                      message: 'Asignado Exitosamente'
                  })
              });
              enviando = True;   
          });  
      }
    }


function miFuncDelete(accion, data) {
    $('input[name="action"]').val(accion);
    $('input[name="id"]').val(data);
    if (enviando == false){
        $('#EppAnular').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            console.log(FormData);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                $('#myModalAsignar').modal('hide');
                tblRequeriTrab.ajax.reload();
                tblAsignarTrab.ajax.reload();
                iziToast.error({
                    position: 'topRight',
                    message: 'Epp Anulado'
                });
            });
            enviando = True;   
        });  
    }
}