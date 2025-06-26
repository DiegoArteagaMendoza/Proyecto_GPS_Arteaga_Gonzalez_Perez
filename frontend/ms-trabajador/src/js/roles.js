document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('rolesTableBody');

    // Mostrar estado de carga
    tableBody.innerHTML = '<tr><td colspan="3" style="text-align: center;">Cargando roles...</td></tr>';

    fetch('https://ms-trabajador-production.up.railway.app/roles/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los roles');
            }
            return response.json();
        })
        .then(data => {
            // Limpiar tabla
            tableBody.innerHTML = '';

            if (data.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="3" style="text-align: center;">No se encontraron roles</td></tr>';
                return;
            }

            data.forEach(rol => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${rol.id_rol || ''}</td>
                    <td>${rol.nombre_rol || ''}</td>
                    <td>${rol.descripcion || ''}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Hubo un error:', error);
            tableBody.innerHTML = `<tr><td colspan="3" style="text-align: center; color: red;">${error.message}</td></tr>`;
        });
});