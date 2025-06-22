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

    function setupEventListeners() {1
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
            // Show loading state
            workersTableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Cargando trabajadores...</td></tr>';

            const response = await fetch('https://ms-trabajador-production.up.railway.app/trabajador/');
            if (!response.ok) {
                throw new Error('Error al cargar los trabajadores');
            }

            allWorkers = await response.json();
            filteredWorkers = [...allWorkers];

            // Reset pagination
            currentPage = 1;
            renderWorkers();

        } catch (error) {
            console.error('Error:', error);
            workersTableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: red;">${error.message}</td></tr>`;
        }
    }

    function filterWorkers() {
        const searchTerm = searchInput.value.toLowerCase();

        if (searchTerm === '') {
            filteredWorkers = [...allWorkers];
        } else {
            filteredWorkers = allWorkers.filter(worker =>
                worker.nombre.toLowerCase().includes(searchTerm) ||
                worker.apellido.toLowerCase().includes(searchTerm) ||
                worker.rut.toLowerCase().includes(searchTerm) ||
                worker.rol.toLowerCase().includes(searchTerm)
            );
        }

        currentPage = 1;
        renderWorkers();
    }

    function renderWorkers() {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const workersToShow = filteredWorkers.slice(startIndex, endIndex);

        if (workersToShow.length === 0) {
            workersTableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No se encontraron trabajadores</td></tr>';
        } else {
            workersTableBody.innerHTML = workersToShow.map(worker => `
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

            // Add event listeners to action buttons
            document.querySelectorAll('.edit-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const workerId = e.currentTarget.getAttribute('data-id');
                    editWorker(workerId);
                });
            });

            document.querySelectorAll('.delete-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const workerId = e.currentTarget.getAttribute('data-id');
                    confirmDelete(workerId);
                });
            });
        }

        // Update pagination controls
        updatePaginationControls();
    }

    function updatePaginationControls() {
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage * itemsPerPage >= filteredWorkers.length;
        pageInfo.textContent = `Página ${currentPage} de ${Math.ceil(filteredWorkers.length / itemsPerPage)}`;
    }

    function formatRUT(rut) {
        if (!rut) return '';

        // Remove any existing formatting
        rut = rut.replace(/\./g, '').replace(/\-/g, '').toUpperCase();

        if (rut.length > 1) {
            const dv = rut.slice(-1);
            const body = rut.slice(0, -1);
            const formattedBody = body.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
            return `${formattedBody}-${dv}`;
        }
        return rut;
    }

    function editWorker(workerId) {
        // Redirect to edit page or show edit modal
        alert(`Editar trabajador con ID: ${workerId}`);
        // window.location.href = `editarTrabajador.html?id=${workerId}`;
    }

    async function confirmDelete(workerId) {
        if (confirm('¿Está seguro que desea eliminar este trabajador?')) {
            try {
                const response = await fetch(`https://ms-trabajador-production.up.railway.app/trabajador/${workerId}/`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    throw new Error('Error al eliminar el trabajador');
                }

                alert('Trabajador eliminado exitosamente');
                loadWorkers();
            } catch (error) {
                console.error('Error:', error);
                alert(error.message || 'Hubo un error al eliminar el trabajador');
            }
        }
    }
});