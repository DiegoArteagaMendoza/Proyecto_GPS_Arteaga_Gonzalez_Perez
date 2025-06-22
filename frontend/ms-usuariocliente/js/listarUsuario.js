document.addEventListener('DOMContentLoaded', async () => {
    const tableBody = document.querySelector('#usuariosTable tbody');

    try {
        const response = await fetch('https://ms-usuariocliente-production.up.railway.app/usuarios/');
        const usuarios = await response.json();

        if (!Array.isArray(usuarios)) {
            throw new Error("La respuesta no es una lista de usuarios");
        }

        usuarios.forEach(usuario => {
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${usuario.id_usuario}</td>
                <td>${usuario.rut}</td>
                <td>${usuario.nombre}</td>
                <td>${usuario.apellido}</td>
                <td>${usuario.correo}</td>
                <td>${usuario.telefono || ''}</td>
                <td>${usuario.rol}</td>
                <td>${usuario.estado ? 'Activo' : 'Inactivo'}</td>
                <td>${new Date(usuario.fecha_registro).toLocaleString()}</td>
            `;

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error al cargar usuarios:', error);
        const row = document.createElement('tr');
        row.innerHTML = `<td colspan="9">Error al cargar usuarios</td>`;
        tableBody.appendChild(row);
    }
});
