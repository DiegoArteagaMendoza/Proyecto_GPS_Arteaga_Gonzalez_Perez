document.getElementById("registro-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const direccion = document.getElementById("direccion").value.trim();
    const comuna = document.getElementById("comuna").value.trim();

    const payload = {
        nombre_farmacia: nombre,
        direccion: direccion,
        comuna: comuna
    };

    try {
        const response = await fetch("https://ms-farmacia-production.up.railway.app/farmacias/registrar/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        // Mostrar resultado con formato mejorado
        const output = document.getElementById("registro-output");
        if (response.ok) {
            output.innerHTML = `
                <div class="success-message">
                    <h3>¡Farmacia registrada exitosamente!</h3>
                    <p><strong>Nombre:</strong> ${result.nombre_farmacia || nombre}</p>
                    <p><strong>Dirección:</strong> ${result.direccion || direccion}</p>
                    <p><strong>Comuna:</strong> ${result.comuna || comuna}</p>
                </div>
            `;
            // Limpiar formulario si fue exitoso
            document.getElementById("registro-form").reset();
        } else {
            output.innerHTML = `
                <div class="error-message">
                    <h3>Error al registrar</h3>
                    <p>${result.message || 'Error desconocido'}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error("Error al registrar farmacia:", error);
        document.getElementById("registro-output").innerHTML = `
            <div class="error-message">
                <h3>Error de conexión</h3>
                <p>No se pudo conectar con el servidor</p>
            </div>
        `;
    }
});