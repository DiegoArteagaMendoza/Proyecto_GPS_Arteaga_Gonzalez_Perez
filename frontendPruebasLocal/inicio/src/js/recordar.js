document.getElementById('recordarBtn').addEventListener('click', () => {
    fetch('http://localhost:8004/usuarios/recordar/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.json(); // si esperas JSON
        })
        .then(data => {
            // Mostrar los datos en el div
            document.getElementById('respuesta').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('respuesta').innerText = 'Error: ' + error.message;
        });
});
