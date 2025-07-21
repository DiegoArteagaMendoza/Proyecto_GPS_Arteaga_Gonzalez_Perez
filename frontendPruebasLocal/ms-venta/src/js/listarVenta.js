document.addEventListener('DOMContentLoaded', function () {
    fetch('https://ms-venta-production.up.railway.app/listar/venta/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener ventas');
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
                    <td>${item.id_venta}</td>
                    <td>${item.fecha_venta}</td>
                    <td>${item.rut_cliente}</td>
                    <td>$${item.total_venta}</td>
                    <td>${item.metodo_pago}</td>
                    <td>${item.estado_venta}</td>
                    <td>${item.farmacia}</td>
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
                <tr><td colspan="6" style="text-align:center; color:red;">Error al cargar ventas</td></tr>
            `;
        });
});


// document.addEventListener('DOMContentLoaded', function () {
//     fetch('https://ms-venta-production.up.railway.app/listar/venta/')
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Error al obtener ventas');
//             }
//             return response.json();
//         })
//         .then(data => {
//             const tableBody = document.querySelector('#bodegasTable tbody');
//             tableBody.innerHTML = ''; // limpiar tabla

//             if (data.length === 0) {
//                 const row = document.createElement('tr');
//                 row.innerHTML = `
//                     <td colspan="6" style="text-align:center;">No hay datos disponibles</td>
//                 `;
//                 tableBody.appendChild(row);
//                 return;
//             }

//             data.forEach(item => {
//                 // Formatear la fecha
//                 const fechaOriginal = new Date(item.fecha_venta);
//                 const dia = fechaOriginal.getDate().toString().padStart(2, '0');
//                 const mes = (fechaOriginal.getMonth() + 1).toString().padStart(2, '0');
//                 const año = fechaOriginal.getFullYear();
//                 const horas = fechaOriginal.getHours().toString().padStart(2, '0');
//                 const minutos = fechaOriginal.getMinutes().toString().padStart(2, '0');

//                 const fechaFormateada = `${dia}/${mes}/${año} ${horas}:${minutos}`;

//                 const row = document.createElement('tr');
//                 row.innerHTML = `
//                     <td>${item.id_venta}</td>
//                     <td>${fechaFormateada}</td>
//                     <td>${item.rut_cliente}</td>
//                     <td>$${item.total_venta}</td>
//                     <td>${item.metodo_pago}</td>
//                     <td>${item.estado_venta}</td>
//                     <td>${item.farmacia}</td>
//                 `;
//                 // <td>${item.producto_id}</td>
//                 // <td>${item.farmacia}</td>

//                 tableBody.appendChild(row);
//             });
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             const tableBody = document.querySelector('#bodegasTable tbody');
//             tableBody.innerHTML = `
//                 <tr><td colspan="6" style="text-align:center; color:red;">Error al cargar ventas</td></tr>
//             `;
//         });
// });