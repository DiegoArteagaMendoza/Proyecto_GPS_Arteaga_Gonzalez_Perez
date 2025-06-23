// Función para cerrar el modal
function closeModal() {
    const modal = document.querySelector('.modal-overlay');
    if (modal) modal.remove();
}

// Función para obtener las farmacias
async function fetchFarmacias() {
    try {
        const response = await fetch('https://ms-farmacia-production.up.railway.app/farmacias/');
        if (!response.ok) throw new Error('Error al cargar farmacias');

        const farmacias = await response.json();
        return farmacias.map(farmacia => ({
            id_farmacia: farmacia.id_farmacia,
            nombre: farmacia.nombre_farmacia,
            direccion: farmacia.direccion,
            comuna: farmacia.comuna
        }));
    } catch (error) {
        console.error('Error al obtener farmacias:', error);
        throw error;
    }
}

// Función para abrir el modal de creación
async function openCreateBodegaModal() {
    try {
        const farmacias = await fetchFarmacias();

        const modalHtml = `
            <div class="modal-overlay">
                <div class="modal-container">
                    <div class="modal-header">
                        <h3>Registrar nueva bodega</h3>
                        <button class="close-modal">&times;</button>
                    </div>
                    <div class="modal-body">
                        <form id="bodegaForm">
                            <div class="form-group">
                                <label>Nombre de bodega</label>
                                <input type="text" id="nombre" placeholder="Ingrese nombre de la nueva bodega" required>
                            </div>
                            <div class="form-group">
                                <label>Dirección de la bodega</label>
                                <input type="text" id="ubicacion" placeholder="Ingrese la dirección de la bodega" required>
                            </div>
                            <div class="form-group">
                                <label>Farmacia perteneciente</label>
                                <select id="farmacia" required>
                                    <option value="">Seleccione una farmacia</option>
                                    ${farmacias.map(f => `
                                        <option value="${f.id_farmacia}">
                                            ${f.nombre} - ${f.comuna} (${f.direccion})
                                        </option>
                                    `).join('')}
                                </select>
                            </div>
                            <div class="form-actions">
                                <button type="button" class="cancel-btn">Cancelar</button>
                                <button type="submit" class="submit-btn">Registrar Bodega</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Event listeners para el modal
        document.querySelector('.close-modal').addEventListener('click', closeModal);
        document.querySelector('.cancel-btn').addEventListener('click', closeModal);
        document.getElementById('bodegaForm').addEventListener('submit', handleFormSubmit);

    } catch (error) {
        console.error('Error al abrir modal:', error);
        alert('Error al cargar el formulario: ' + error.message);
    }
}

// Función para manejar el envío del formulario
async function handleFormSubmit(e) {
    e.preventDefault();

    const submitBtn = document.querySelector('#bodegaForm .submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Registrando...';

    try {
        const formData = {
            nombre: document.getElementById('nombre').value.trim(),
            ubicacion: document.getElementById('ubicacion').value.trim(),
            farmacia: document.getElementById('farmacia').value
        };

        if (!formData.nombre || !formData.ubicacion || !formData.farmacia) {
            throw new Error('Todos los campos son obligatorios');
        }

        const response = await fetch('https://ms-inventario-production-98de.up.railway.app/bodegas/registrar/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Error al registrar la bodega');
        }

        alert('Bodega registrada exitosamente');
        closeModal();
        loadBodegas(); // Recargar la lista de bodegas

    } catch (error) {
        console.error('Error al registrar bodega:', error);
        alert('Error: ' + error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Registrar Bodega';
    }
}