document.getElementById('scanButton').addEventListener('click', function() {
    const videoElement = document.createElement('video');
    document.body.appendChild(videoElement);

    const scanner = new Instascan.Scanner({ video: videoElement });

    scanner.addListener('scan', function(content) {
      alert('Código QR escaneado: ' + content);
    });

    Instascan.Camera.getCameras().then(function(cameras) {
      if (cameras.length > 0) {
        scanner.start(cameras[0]);
      } else {
        alert('No se encontraron cámaras disponibles.');
      }
    });
});
