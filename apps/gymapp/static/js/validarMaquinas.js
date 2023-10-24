document.getElementById("btnEnviar").addEventListener("click", function(event) {
    event.preventDefault();
  
    var nombre = document.getElementById("txtMaquina").value;
    var zona = document.getElementById("txtZona").value;
 
    
    if (nombre === "" || zona === "") {
      var alerta = document.getElementById("alerta");
      alerta.innerHTML = "Por favor, complete todos los campos.";
      alerta.style.display = "block";
      
      setTimeout(function() {
        alerta.style.display = "none";
      }, 6000);
    } else {

      document.getElementById("agregarMaquinaForm").submit();
    }
    
  });
