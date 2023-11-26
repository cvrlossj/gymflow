document.addEventListener('DOMContentLoaded', function() {
  let cameraActive = false;
  const cameraContainer = document.getElementById('cameraContainer');
  const videoElement = document.createElement('video');
  const machineDetails = document.getElementById('machineDetails');
  const machineName = document.getElementById('machineName');
  const machineDescription = document.getElementById('machineDescription');
  const machineID = document.getElementById('machineID');
  const machineZone = document.getElementById('machineZone');
  const tutorialIframe = document.getElementById('tutorialIframe');

  document.getElementById('scanButton').addEventListener('click', function() {
    if (!cameraActive) {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
          .then(function(stream) {
            videoElement.srcObject = stream;
            videoElement.setAttribute('autoplay', '');
            videoElement.setAttribute('playsinline', ''); // For iOS support
            cameraContainer.appendChild(videoElement);
            cameraContainer.style.display = 'block';

            const scanner = new Instascan.Scanner({ video: videoElement });
            scanner.addListener('scan', function(content) {
              const qrContent = content;
              const qrData = JSON.parse(qrContent);

              // Actualizar el contenido del modal con la información del código QR
              machineName.innerText = qrData.nombre;
              machineDescription.innerText = qrData.descripcion;
              machineID.innerText = qrData.id;
              machineZone.innerText = qrData.zona_muscular;
              tutorialIframe.src = `https://www.youtube.com/embed/${qrData.enlace_tutorial}`;

              // Mostrar los detalles de la máquina en el modal
              machineDetails.style.display = 'block';

              // Detener la cámara y limpiar
              cameraActive = false;
              stream.getTracks().forEach(track => track.stop());
              cameraContainer.style.display = 'none';
            });

            Instascan.Camera.getCameras().then(function(cameras) {
              if (cameras.length > 0) {
                cameraActive = true;
                scanner.start(cameras[0]);
              } else {
                alert('No se encontraron cámaras disponibles.');
              }
            });
          })
          .catch(function(error) {
            console.error('Error al acceder a la cámara:', error);
          });
      } else {
        alert('El navegador no soporta la funcionalidad de la cámara.');
      }
    }
  });
});
