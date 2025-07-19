document.addEventListener('DOMContentLoaded', async function () {
    const formContainer = document.getElementById('formContainer');
    const successContainer = document.getElementById('successContainer');
    const ventaForm = document.getElementById('ventaForm');
    const addProductBtn = document.getElementById('addProductBtn');
    const detalleContainer = document.getElementById('detalle-productos-container');

    // Ocultar el mensaje de éxito al inicio
    successContainer.style.display = 'none';

    // Cargar farmacias
    try {
        const farmacias = await fetchFarmacias();
        const farmaciaSelect = document.getElementById('farmacia');

        // Limpiar select
        farmaciaSelect.innerHTML = '<option value="">Seleccione una farmacia</option>';

        // Añadir opciones
        farmacias.forEach(farmacia => {
            const option = document.createElement('option');
            option.value = farmacia.nombre_farmacia;
            option.textContent = farmacia.nombre_farmacia;
            farmaciaSelect.appendChild(option);
        });
    } catch (error) {
        alert('Error al cargar farmacias: ' + error.message);
    }

    // Cargar productos (para el detalle)
    let productos = [];
    try {
        productos = await fetchProductos();
    } catch (error) {
        alert('Error al cargar productos: ' + error.message);
    }

    // Función para agregar un producto al detalle
    addProductBtn.addEventListener('click', () => addProductoDetalle(productos));

    // Agregar un producto por defecto
    addProductoDetalle(productos);

    // Manejar el envío del formulario
    ventaForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const submitBtn = ventaForm.querySelector('.submit-btn');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Registrando...';

        try {
            const detalles = [];
            let totalVenta = 0;

            // Recoger datos de los productos
            const productoItems = document.querySelectorAll('.producto-item');
            productoItems.forEach(item => {
                const select = item.querySelector('.producto-select');
                const cantidadInput = item.querySelector('.cantidad-input');
                const precioInput = item.querySelector('.precio-unitario-input');

                const productoId = select.value;
                const cantidad = parseFloat(cantidadInput.value);
                const precio = parseFloat(precioInput.value);
                const nombre = select.options[select.selectedIndex].text;
                const subtotal = cantidad * precio;
                totalVenta += subtotal;

                detalles.push({
                    id_producto: productoId,
                    nombre_producto: nombre,
                    cantidad: cantidad,
                    precio_unitario: precio,
                    subtotal: subtotal
                });
            });

            const ventaData = {
                rut_cliente: document.getElementById('rut_comprador').value,
                numero_boleta: document.getElementById('numero_boleta').value,
                metodo_pago: document.getElementById('metodo_pago').value,
                estado_venta: document.getElementById('estado').value,
                farmacia: document.getElementById('farmacia').value,
                detalles: detalles,
                total_venta: totalVenta
            };

            // Enviar datos al servidor
            const response = await fetch('http://localhost:8005/realizar/venta/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(ventaData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Error al registrar la venta');
            }

            // Mostrar mensaje de éxito
            formContainer.style.display = 'none';
            successContainer.style.display = 'block';

        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-check"></i> Registrar Venta';
        }
    });
});

// Función para agregar un producto al detalle
function addProductoDetalle(productos) {
    const container = document.getElementById('detalle-productos-container');
    const index = container.children.length;

    const div = document.createElement('div');
    div.className = 'producto-item';
    div.innerHTML = `
                <div class="form-group">
                    <label>Producto:</label>
                    <select class="producto-select" required>
                        <option value="">Seleccione producto</option>
                        ${productos.map(p => `
                            <option value="${p.id_producto}" data-precio="${p.precio_venta}">
                                ${p.nombre}
                            </option>
                        `).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label>Cantidad:</label>
                    <input type="number" class="cantidad-input" step="1" min="1" value="1" required>
                </div>
                <div class="form-group">
                    <label>Precio Unitario:</label>
                    <input type="number" class="precio-unitario-input" step="0.01" min="0" required>
                </div>
                <button type="button" class="remove-product-btn">
                    <i class="fas fa-trash"></i> Eliminar
                </button>
            `;

    container.appendChild(div);

    // Evento para eliminar el producto
    const removeBtn = div.querySelector('.remove-product-btn');
    removeBtn.addEventListener('click', () => div.remove());

    // Evento para actualizar el precio cuando se selecciona un producto
    const select = div.querySelector('.producto-select');
    const precioInput = div.querySelector('.precio-unitario-input');

    select.addEventListener('change', function () {
        const selectedOption = this.options[this.selectedIndex];
        const precio = selectedOption.dataset.precio || '';
        precioInput.value = precio;
    });
}

// Funciones para obtener farmacias y productos
async function fetchFarmacias() {
    const response = await fetch('http://localhost:8006/farmacias/');
    if (!response.ok) throw new Error("Error al obtener farmacias");
    return await response.json();
}

async function fetchProductos() {
    const response = await fetch('http://localhost:8002/productos/');
    if (!response.ok) throw new Error("Error al obtener productos");
    return await response.json();
}