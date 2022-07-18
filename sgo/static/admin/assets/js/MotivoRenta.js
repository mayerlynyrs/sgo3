
  function validar(obj){
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