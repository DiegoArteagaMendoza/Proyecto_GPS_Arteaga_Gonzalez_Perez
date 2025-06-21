document.addEventListener('DOMContentLoaded', function () {
    fetch('https://ms-trabajador-production-f278.up.railway.app/roles/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los roles');
            }
            return response.json();
        })
        .then(data => {
            const tableBody = document.querySelector('#rolesTable tbody');
            data.forEach(rol => {
                const row = document.createElement('tr');
                row.innerHTML = `
            <td>${rol.id_rol}</td>
            <td>${rol.nombre_rol}</td>
            <td>${rol.descripcion}</td>
          `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Hubo un error:', error);
        });
});
  