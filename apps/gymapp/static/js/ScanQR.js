document.getElementById('scanButton').addEventListener('click', function() {
    const videoElement = document.createElement('video');
    document.body.appendChild(videoElement);

    const scanner = new Instascan.Scanner({ video: videoElement });

    scanner.addListener('scan', function(content) {
      // Cuando se escanea un código QR, extraer la URL
      const url = content;

      // Abrir la URL en una nueva pestaña o ventana del navegador
      window.open(url, '_blank');
    });

    Instascan.Camera.getCameras().then(function(cameras) {
      if (cameras.length > 0) {
        scanner.start(cameras[0]);
      } else {
        alert('No se encontraron cámaras disponibles.');
      }
    });
  });