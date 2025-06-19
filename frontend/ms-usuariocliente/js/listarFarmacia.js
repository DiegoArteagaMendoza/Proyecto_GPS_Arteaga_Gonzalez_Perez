document.addEventListener('DOMContentLoaded', function () {
    fetch('http://ms-farmacia-production-c583.up.railway.app/farmacias/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener farmacias');
            }
            return response.json();
        })
        .then(data => {
            const tbody = document.querySelector('#farmaciasTable tbody');
            tbody.innerHTML = '';
            data.forEach(farmacia => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${farmacia.id_farmacia}</td>
                    <td>${farmacia.nombre_farmacia}</td>
                    <td>${farmacia.direccion}</td>
                    <td>${farmacia.comuna || ''}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
