// script.js
document.addEventListener('DOMContentLoaded', async () => {
    const tableBody = document.querySelector('#usuariosTable tbody');

    // Mostrar estado de carga
    showLoadingState(tableBody);

    try {
        const usuarios = await fetchUsuarios();

        if (usuarios.length === 0) {
            showNoResults(tableBody);
            return;
        }

        renderUsuarios(tableBody, usuarios);
    } catch (error) {
        showErrorState(tableBody, error);
    }
});

async function fetchUsuarios() {
  const response = await fetch('http://localhost:8004/usuarios/'); // https://ms-usuariocliente-production.up.railway.app/usuarios/

    if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    if (!Array.isArray(data)) {
        throw new Error("Formato de datos inválido");
    }

    return data;
}

function renderUsuarios(tableBody, usuarios) {
    tableBody.innerHTML = '';

    usuarios.forEach(usuario => {
        const row = document.createElement('tr');
        const estadoClass = usuario.estado ? 'status-active' : 'status-inactive';

        row.innerHTML = `
        <td>${formatRUT(usuario.rut) || 'N/A'}</td>
        <td>${capitalize(usuario.nombre) || 'N/A'}</td>
        <td>${capitalize(usuario.apellido) || 'N/A'}</td>
        <td>${usuario.correo?.toLowerCase() || 'N/A'}</td>
        <td>${formatPhone(usuario.telefono) || 'N/A'}</td>
        <td class="${estadoClass}">${usuario.estado ? 'Activo' : 'Inactivo'}</td>
        <td>${formatDate(usuario.fecha_registro) || 'N/A'}</td>
      `;

        tableBody.appendChild(row);
    });
}

// Helper functions
function formatRUT(rut) {
    if (!rut) return '';
    // Implementar lógica de formateo RUT chileno si es necesario
    return rut;
}

function formatPhone(phone) {
    if (!phone) return '';
    // Formatear número de teléfono si es necesario
    return phone;
}

function formatDate(dateString) {
    if (!dateString) return '';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-CL');
    } catch {
        return dateString;
    }
}

function capitalize(str) {
    if (!str) return '';
    return str.toLowerCase().replace(/\b\w/g, char => char.toUpperCase());
}

function showLoadingState(tableBody) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="9" class="loading-state">
          <div class="spinner"></div>
          <span>Cargando usuarios...</span>
        </td>
      </tr>
    `;
}

function showNoResults(tableBody) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="9" class="no-results">
          No se encontraron usuarios registrados
        </td>
      </tr>
    `;
}

function showErrorState(tableBody, error) {
    console.error('Error al cargar usuarios:', error);
    tableBody.innerHTML = `
      <tr>
        <td colspan="9" class="error-state">
          Error al cargar los datos: ${error.message}
        </td>
      </tr>
    `;
  }