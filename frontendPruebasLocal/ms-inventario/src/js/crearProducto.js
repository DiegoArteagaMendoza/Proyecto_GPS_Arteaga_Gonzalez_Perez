// Función para cerrar el modal
function closeModalProducto() {
    const modal = document.querySelector('.modal-overlay');
    if (modal) modal.remove();
}

// Función para abrir el modal
function openCreateProductoModal() {
    const modalHtml = `
        <div class="modal-overlay">
            <div class="modal-container">
                <div class="modal-header">
                    <h3>Registrar nuevo producto</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <form id="productoForm">
                        <div class="form-group">
                            <label>Nombre del producto</label>
                            <input type="text" id="nombreProducto" placeholder="Ingrese nombre" required>
                        </div>
                        <div class="form-group">
                            <label>Descripción</label>
                            <textarea id="descripcionProducto" placeholder="Ingrese descripción" required></textarea>
                        </div>
                        <div class="form-actions">
                            <button type="button" class="cancel-btn">Cancelar</button>
                            <button type="submit" class="submit-btn">Registrar Producto</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);

    document.querySelector('.close-modal').addEventListener('click', closeModalProducto);
    document.querySelector('.cancel-btn').addEventListener('click', closeModalProducto);
    document.getElementById('productoForm').addEventListener('submit', handleProductoSubmit);
}

// Enviar datos al backend
async function handleProductoSubmit(e) {
    e.preventDefault();

    const submitBtn = document.querySelector('#productoForm .submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Registrando...';

    try {
        const formData = {
            nombre: document.getElementById('nombreProducto').value.trim(),
            descripcion: document.getElementById('descripcionProducto').value.trim()
        };

        if (!formData.nombre || !formData.descripcion) {
            throw new Error('Todos los campos son obligatorios');
        }

        const response = await fetch('http://localhost:8002/productos/registrar/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error del backend:', errorData);
            throw new Error(errorData.message || 'Error al registrar el producto');
        }

        alert('Producto registrado exitosamente');
        closeModalProducto();
        loadProductos(); // Recargar productos

    } catch (error) {
        console.error('Error al registrar producto:', error);
        alert('Error: ' + error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Registrar Producto';
    }
}
