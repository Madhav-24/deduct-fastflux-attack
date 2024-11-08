function uploadImage() {
    var input = document.getElementById('uploadInput');
    var file = input.files[0];

    var formData = new FormData();
    formData.append('image', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.fastfluxDetected) {
            alert('Fastflux attack detected! Malicious IP addresses: ' + data.maliciousIPs.join(', '));
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
