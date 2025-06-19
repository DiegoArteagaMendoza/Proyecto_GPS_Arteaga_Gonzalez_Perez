document.addEventListener('DOMContentLoaded', function () {
    const filterType = document.getElementById('filterType');
    const filterInput = document.getElementById('filterInput');
    const filterBtn = document.getElementById('filterBtn');

    // Habilitar/deshabilitar campo de filtro según selección
    filterType.addEventListener('change', function () {
        if (this.value === 'all') {
            filterInput.disabled = true;
            filterBtn.disabled = true;
            filterInput.placeholder = 'Seleccione un filtro';
        } else {
            filterInput.disabled = false;
            filterBtn.disabled = false;

            // Actualizar placeholder según el tipo de filtro
            switch (this.value) {
                case 'rut':
                    filterInput.placeholder = 'Ingrese RUT (ej: 12345678-9)';
                    break;
                case 'nombre':
                    filterInput.placeholder = 'Ingrese nombre del trabajador';
                    break;
                case 'correo':
                    filterInput.placeholder = 'Ingrese correo electrónico';
                    break;
            }
        }
    });

    // Manejar el evento de filtrar
    filterBtn.addEventListener('click', function () {
        const type = filterType.value;
        const value = filterInput.value.trim();

        if (value === '') {
            alert('Por favor ingrese un valor para filtrar');
            return;
        }

        let endpoint = '';

        switch (type) {
            case 'rut':
                endpoint = `http://ms-trabajador-production-f278.up.railway.app/trabajador/buscar/rut/?rut=${encodeURIComponent(value)}`;
                break;
            case 'nombre':
                endpoint = `http://ms-trabajador-production-f278.up.railway.app/trabajador/buscar/nombre/?nombre=${encodeURIComponent(value)}`;
                break;
            case 'correo':
                endpoint = `http://ms-trabajador-production-f278.up.railway.app/trabajador/buscar/correo/?correo=${encodeURIComponent(value)}`;
                break;
        }

        fetchFilteredData(endpoint);
    });

    // Función para obtener datos filtrados
    async function fetchFilteredData(endpoint) {
        try {
            // Mostrar estado de carga
            document.getElementById('workersTableBody').innerHTML = '<tr><td colspan="6" style="text-align: center;">Buscando trabajadores...</td></tr>';

            const response = await fetch(endpoint);

            if (!response.ok) {
                throw new Error('Error al buscar trabajadores');
            }

            const data = await response.json();

            // Actualizar la tabla con los resultados
            updateTableWithFilteredData(data);

        } catch (error) {
            console.error('Error:', error);
            document.getElementById('workersTableBody').innerHTML = `<tr><td colspan="6" style="text-align: center; color: red;">${error.message}</td></tr>`;
        }
    }

    // Función para actualizar la tabla con datos filtrados
    function updateTableWithFilteredData(workers) {
        const tableBody = document.getElementById('workersTableBody');

        if (workers.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No se encontraron trabajadores</td></tr>';
            return;
        }

        tableBody.innerHTML = workers.map(worker => `
            <tr>
                <td>${worker.nombre}</td>
                <td>${worker.apellido}</td>
                <td>${formatRUT(worker.rut)}</td>
                <td>${worker.rol}</td>
                <td class="${worker.estado ? 'status-active' : 'status-inactive'}">
                    ${worker.estado ? 'Activo' : 'Inactivo'}
                </td>
                <td>
                    <button class="action-btn edit-btn" data-id="${worker.id_trabajador}">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="action-btn delete-btn" data-id="${worker.id_trabajador}">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        // Actualizar controles de paginación (si es necesario)
        document.getElementById('prevBtn').disabled = true;
        document.getElementById('nextBtn').disabled = true;
        document.getElementById('pageInfo').textContent = `Mostrando ${workers.length} resultados`;
    }

    // Función para formatear RUT
    function formatRUT(rut) {
        if (!rut) return '';

        // Eliminar formato existente
        rut = rut.replace(/\./g, '').replace(/\-/g, '').toUpperCase();

        if (rut.length > 1) {
            const dv = rut.slice(-1);
            const body = rut.slice(0, -1);
            const formattedBody = body.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
            return `${formattedBody}-${dv}`;
        }
        return rut;
    }
});