document.addEventListener('DOMContentLoaded', function () {
    const farmaciaSelect = document.getElementById('farmacia');
    const bodegaForm = document.getElementById('bodegaForm');

    // Cargar farmacias desde el endpoint
    fetch('http://ms-farmacia-production-c583.up.railway.app/farmacias/')
        .then(response => {
            if (!response.ok) throw new Error('Error al obtener farmacias');
            return response.json();
        })
        .then(data => {
            data.forEach(farmacia => {
                const option = document.createElement('option');
                option.value = farmacia.id_farmacia; // usamos id para identificar internamente
                option.textContent = farmacia.nombre_farmacia; // mostramos el nombre al usuario
                farmaciaSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error al cargar farmacias:', error);
            alert('No se pudieron cargar las farmacias.');
        });

    // Enviar formulario al backend
    bodegaForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const nombre = document.getElementById('nombre').value.trim();
        const ubicacion = document.getElementById('ubicacion').value.trim();
        const farmaciaNombre = farmaciaSelect.options[farmaciaSelect.selectedIndex].textContent;

        if (!nombre || !ubicacion || !farmaciaNombre || farmaciaNombre === 'Seleccione una farmacia') {
            alert('Por favor complete todos los campos.');
            return;
        }

        const bodegaData = {
            nombre: nombre,
            ubicacion: ubicacion,
            farmacia: farmaciaNombre,
            estado: 1
        };

        fetch('http://ms-inventario-production-98de.up.railway.app/bodegas/registrar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bodegaData)
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => {
                        console.error('Respuesta del servidor:', err);
                        throw new Error('Error al registrar la bodega');
                    });
                }
                return response.json();
            })
            .then(data => {
                alert('Bodega registrada exitosamente.');
                bodegaForm.reset();
            })
            .catch(error => {
                console.error('Error al registrar la bodega:', error);
                alert('Hubo un error al registrar la bodega.');
            });
        
    });
});
