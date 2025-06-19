async function listarFarmacias() {
    try {
        const response = await fetch("http://ms-farmacia-production-c583.up.railway.app/farmacias/");
        const data = await response.json();

        const tbody = document.getElementById("farmacias-body");
        tbody.innerHTML = ''; // Limpiar tabla

        if (response.ok && data.length > 0) {
            data.forEach(farmacia => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${farmacia.nombre_farmacia}</td>
                    <td>${farmacia.direccion}</td>
                    <td>${farmacia.comuna}</td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = `
                <tr>
                    <td colspan="3" class="no-data">No hay farmacias registradas</td>
                </tr>
            `;
        }
    } catch (error) {
        console.error("Error al obtener farmacias:", error);
        document.getElementById("farmacias-body").innerHTML = `
            <tr>
                <td colspan="3" class="error-data">Error al cargar los datos</td>
            </tr>
        `;
    }
}

// Cargar datos al iniciar
document.addEventListener('DOMContentLoaded', listarFarmacias);

// Botón para refrescar
document.getElementById('refresh-btn').addEventListener('click', listarFarmacias);