document.addEventListener('DOMContentLoaded', () => {
    // Cargar productos al inicio
    loadProductos();

    // Escuchar el botón para crear producto
    document.getElementById('createProductoBtn')?.addEventListener('click', openCreateProductoModal);
});

async function loadProductos() {
    const tableBody = document.querySelector('#bodegasTable tbody'); // ID corregido
    showLoadingState(tableBody);

    try {
        const productos = await fetchProductos();
        productos.length > 0
            ? renderProductos(tableBody, productos)
            : showNoResults(tableBody);
    } catch (error) {
        showErrorState(tableBody, error);
    }
}
async function fetchProductos() {
    const response = await fetch('https://ms-inventario-production-98de.up.railway.app/productos/');
    if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

    const data = await response.json();
    if (!Array.isArray(data)) throw new Error("Formato de datos inválido");
    return data;
}

function renderProductos(tableBody, productos) {
    tableBody.innerHTML = productos.map(prod => `
        <tr>
            <td>${capitalize(prod.nombre) || 'N/A'}</td>
            <td>${prod.descripcion || 'Sin descripción'}</td>
        </tr>
    `).join('');
}

const capitalize = str => str ? str.toLowerCase().replace(/\b\w/g, c => c.toUpperCase()) : '';

function showLoadingState(tableBody) {
    tableBody.innerHTML = `<tr><td colspan="2">Cargando productos...</td></tr>`;
}

function showNoResults(tableBody) {
    tableBody.innerHTML = `<tr><td colspan="2">No se encontraron productos</td></tr>`;
}

function showErrorState(tableBody, error) {
    console.error('Error al cargar productos:', error);
    tableBody.innerHTML = `<tr><td colspan="2">Error: ${error.message}</td></tr>`;
}
