document.addEventListener('DOMContentLoaded', function () {
    let currentPage = 1;
    const itemsPerPage = 10;
    let allWorkers = [];
    let filteredWorkers = [];

    // DOM Elements
    const workersTableBody = document.getElementById('workersTableBody');
    const searchInput = document.getElementById('searchInput');
    const refreshBtn = document.getElementById('refreshBtn');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const pageInfo = document.getElementById('pageInfo');

    // Initialize
    loadWorkers();
    setupEventListeners();

    function setupEventListeners() {
        searchInput.addEventListener('input', filterWorkers);
        refreshBtn.addEventListener('click', loadWorkers);
        prevBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                renderWorkers();
            }
        });
        nextBtn.addEventListener('click', () => {
            if (currentPage * itemsPerPage < filteredWorkers.length) {
                currentPage++;
                renderWorkers();
            }
        });
    }

    async function loadWorkers() {
        try {
            workersTableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Cargando trabajadores...</td></tr>';

            const response = await fetch('http://localhost:8003/trabajador/');
            if (!response.ok) {
                throw new Error('Error al cargar los trabajadores');
            }

            allWorkers = await response.json();
            filteredWorkers = [...allWorkers];
            currentPage = 1;
            renderWorkers();

        } catch (error) {
            console.error('Error:', error);
            workersTableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: red;">${error.message}</td></tr>`;
        }
    }

    function filterWorkers() {
        const searchTerm = searchInput.value.toLowerCase();
        filteredWorkers = searchTerm === ''
            ? [...allWorkers]
            : allWorkers.filter(worker =>
                worker.nombre.toLowerCase().includes(searchTerm) ||
                worker.apellido.toLowerCase().includes(searchTerm) ||
                (worker.rut && worker.rut.toLowerCase().includes(searchTerm)) ||
                (worker.rol && worker.rol.toLowerCase().includes(searchTerm))
            );

        currentPage = 1;
        renderWorkers();
    }

    function renderWorkers() {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const workersToShow = filteredWorkers.slice(startIndex, endIndex);

        workersTableBody.innerHTML = workersToShow.length === 0
            ? '<tr><td colspan="6" style="text-align: center;">No se encontraron trabajadores</td></tr>'
            : workersToShow.map(worker => `
                <tr>
                    <td>${worker.nombre || ''}</td>
                    <td>${worker.apellido || ''}</td>
                    <td>${worker.rut ? formatRUT(worker.rut) : ''}</td>
                    <td>${worker.rol || ''}</td>
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

        // Add event listeners
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', () => editWorker(btn.getAttribute('data-id')));
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', () => confirmDelete(btn.getAttribute('data-id')));
        });

        updatePaginationControls();
    }

    function updatePaginationControls() {
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage * itemsPerPage >= filteredWorkers.length;
        pageInfo.textContent = `Página ${currentPage} de ${Math.ceil(filteredWorkers.length / itemsPerPage)}`;
    }

    function formatRUT(rut) {
        if (!rut) return '';
        rut = rut.replace(/\./g, '').replace(/\-/g, '').toUpperCase();
        if (rut.length > 1) {
            const dv = rut.slice(-1);
            const body = rut.slice(0, -1);
            return `${body.replace(/\B(?=(\d{3})+(?!\d))/g, '.')}-${dv}`;
        }
        return rut;
    }

    function editWorker(workerId) {
        alert(`Editar trabajador con ID: ${workerId}`);
        // window.location.href = `editarTrabajador.html?id=${workerId}`;
    }

    async function confirmDelete(workerId) {
        if (confirm('¿Está seguro que desea desactivar este trabajador?')) {
            try {
                const response = await fetch('http://localhost:8003/trabajador/desactivar/', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id_trabajador: workerId })
                });

                if (!response.ok) {
                    throw new Error('Error al desactivar el trabajador');
                }

                alert('Trabajador desactivado exitosamente');
                loadWorkers();
            } catch (error) {
                console.error('Error:', error);
                alert(error.message || 'Hubo un error al desactivar el trabajador');
            }
        }
    }
});