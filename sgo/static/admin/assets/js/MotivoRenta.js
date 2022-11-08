
  function validar(obj){

    
    var getDate = function (input) {
        return new Date(input.date.valueOf());
    }
  
    divC = document.getElementById("divmotivo");
    if(obj.checked==true){
        divC.style.display = "";
    }else{
        divC.style.display = "none";
        document.getElementById("NuevoMotivo").value = "";

    }
  }
  function validar2(obj){
    divRenta = document.getElementById("divrenta");
    if(obj.checked==true){
        divRenta.style.display = "";
    }else{
        divRenta.style.display = "none"; 
        document.getElementById("NuevaRenta").value = "";
    }
  }


  function mensualdiario() {
    if (document.getElementById('mensual').checked) {
        document.getElementById('tipocontrato').style.display = 'block';
        document.getElementById('fechatermino').style.display = 'block';
        document.getElementById('sueldo').style.display = 'block';
        document.getElementById('valores_diario').style.display = 'none';
      $("#id_tipo_documento").val('');
    }
    else{
      document.getElementById('tipocontrato').style.display = 'none';
      $("#id_tipo_documento").val('8');
      document.getElementById('fechatermino').style.display = 'none';
      document.getElementById('sueldo').style.display = 'none';
      document.getElementById('valores_diario').style.display = 'block';
    } 
 
}
function ver_documento(){

var elemento = document.getElementById("id_tipo_documento").value
  if (elemento == ""){
    iziToast.error({
      message: 'Debe ingresar Tipo Contrato',
      position: 'topRight',
    });
}


// var sueldo_base = document.getElementById("id_sueldo_base").value
//   if (sueldo_base == ""){
//     iziToast.error({
//       message: 'Debe ingresar Sueldo Base',
//       position: 'topRight',
//     });
// }
}