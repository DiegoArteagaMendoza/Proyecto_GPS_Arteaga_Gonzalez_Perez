document.addEventListener('DOMContentLoaded', () => {
    // Cargar bodegas al inicio
    loadBodegas();

    // Agregar event listener al botón de creación
    document.getElementById('createBodegaBtn')?.addEventListener('click', openCreateBodegaModal);
});

async function loadBodegas() {
    const tableBody = document.querySelector('#bodegasTable tbody');
    showLoadingState(tableBody);

    try {
        const bodegas = await fetchBodegas();
        bodegas.length > 0
            ? renderBodegas(tableBody, bodegas)
            : showNoResults(tableBody);
    } catch (error) {
        showErrorState(tableBody, error);
    }
}

async function fetchBodegas() {
    const response = await fetch('https://ms-inventario-production-98de.up.railway.app/bodegas/');
    if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

    const data = await response.json();
    if (!Array.isArray(data)) throw new Error("Formato de datos inválido");

    return data;
}

function renderBodegas(tableBody, bodegas) {
    tableBody.innerHTML = bodegas.map(bodega => {
        const estadoClass = bodega.estado == 1 ? 'status-active' : 'status-inactive';
        const estadoText = bodega.estado == 1 ? 'Activa' : 'Inactiva';

        return `
            <tr>
                <td>${bodega.id_bodega || 'N/A'}</td>
                <td>${capitalize(bodega.nombre) || 'N/A'}</td>
                <td>${bodega.ubicacion || 'No especificada'}</td>
                <td>${capitalize(bodega.farmacia) || 'N/A'}</td>
                <td class="${estadoClass}">${estadoText}</td>
                
            </tr>
        `;
    }).join('');

    // Agregar event listeners
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', () => viewBodega(btn.dataset.id));
    });
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => editBodega(btn.dataset.id));
    });
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => confirmDeleteBodega(btn.dataset.id));
    });
}

// Helper functions
const capitalize = str => str ? str.toLowerCase().replace(/\b\w/g, char => char.toUpperCase()) : '';

function showLoadingState(tableBody) {
    tableBody.innerHTML = `
        <tr>
            <td colspan="6" class="loading-state">
                <div class="spinner"></div> Cargando bodegas...
            </td>
        </tr>
    `;
}

function showNoResults(tableBody) {
    tableBody.innerHTML = `
        <tr>
            <td colspan="6" class="no-results">
                No se encontraron bodegas registradas
            </td>
        </tr>
    `;
}

function showErrorState(tableBody, error) {
    console.error('Error al cargar bodegas:', error);
    tableBody.innerHTML = `
        <tr>
            <td colspan="6" class="error-state">
                Error al cargar los datos: ${error.message}
            </td>
        </tr>
    `;
}

// Funciones para acciones
function viewBodega(bodegaId) {
    console.log(`Ver bodega ID: ${bodegaId}`);
    // Implementar lógica para ver detalles
}

function editBodega(bodegaId) {
    console.log(`Editar bodega ID: ${bodegaId}`);
    // Implementar lógica para editar
}

function confirmDeleteBodega(bodegaId) {
    if (confirm('¿Está seguro que desea eliminar esta bodega?')) {
        console.log(`Eliminar bodega ID: ${bodegaId}`);
        // Implementar lógica para eliminar
    }
}