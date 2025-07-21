document.addEventListener('DOMContentLoaded', function () {
    fetch('http://localhost:8002/inventario/mostrar/disponibles/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener inventario');
            }
            return response.json();
        })
        .then(data => {
            const tableBody = document.querySelector('#bodegasTable tbody');
            tableBody.innerHTML = ''; // limpiar tabla

            if (data.length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td colspan="6" style="text-align:center;">No hay datos disponibles</td>
                `;
                tableBody.appendChild(row);
                return;
            }

            data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.nombre_producto}</td>
                    <td>${item.descripcion}</td>
                    <td>${item.cantidad}</td>
                    <td>$${item.costo_unitario}</td>
                `;
                // <td>${item.producto_id}</td>

                // <td>${item.farmacia}</td>

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            const tableBody = document.querySelector('#bodegasTable tbody');
            tableBody.innerHTML = `
                <tr><td colspan="6" style="text-align:center; color:red;">Error al cargar inventario</td></tr>
            `;
        });
});
