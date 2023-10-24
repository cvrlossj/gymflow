let cameraActive = false; 
const cameraContainer = document.getElementById('cameraContainer');

document.getElementById('scanButton').addEventListener('click', function() {
  const videoElement = document.createElement('video');
  document.body.appendChild(videoElement);

  const scanner = new Instascan.Scanner({ video: videoElement });

  scanner.addListener('scan', function(content) {
    if (!cameraActive) {
      return; 
    }

    const url = content;


    cameraActive = false;
    videoElement.srcObject.getTracks().forEach(track => track.stop());
    cameraContainer.style.display = 'none';
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