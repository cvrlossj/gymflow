
let cameraActive = false;

  document.getElementById('scanButton').addEventListener('click', function() {
    const videoElement = document.createElement('video');
    document.body.appendChild(videoElement);

    const scanner = new Instascan.Scanner({ video: videoElement });

    scanner.addListener('scan', function(content) {
      if (!cameraActive) {
        return; // Si la cámara no está activa, no hagas nada
      }

      // Cuando se escanea un código QR, extraer la URL
      const url = content;


      cameraActive = false;
      videoElement.srcObject.getTracks().forEach(track => track.stop());

   
      window.open(url, '_blank');
    });

    Instascan.Camera.getCameras().then(function(cameras) {
      if (cameras.length > 0) {
        cameraActive = true; 
        scanner.start(cameras[0]);
      } else {
        alert('No se encontraron cámaras disponibles.');
      }
    });
  });