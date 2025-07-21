document.getElementById('recordarBtn').addEventListener('click', () => {
    // Mostrar estado de carga
    document.getElementById('respuesta').innerHTML = '<div class="loading">Procesando...</div>';

    fetch('http://localhost:8004/usuarios/recordar/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.json();
        })
        .then(data => {
            // Mostrar mensaje de éxito con estilo
            document.getElementById('respuesta').innerHTML = `
                <div class="success-message">
                    <span class="icon">✓</span>
                    Pacientes recordados exitosamente
                </div>
            `;

            // Opcional: Mostrar también los datos en consola para debugging
            console.log('Respuesta del servidor:', data);
        })
        .catch(error => {
            // Mostrar mensaje de error con estilo
            document.getElementById('respuesta').innerHTML = `
                <div class="error-message">
                    <span class="icon">✗</span>
                    Error al recordar pacientes: ${error.message}
                </div>
            `;
        });
});