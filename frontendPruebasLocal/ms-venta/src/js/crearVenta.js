document.getElementById('crearVenta')?.addEventListener('click', openCreateVentaModal);

async function openCreateVentaModal() {
    try {
        const farmacias = await fetchFarmacias();
        const productos = await fetchProductos();

        const modalHtml = `
            <div class="modal-overlay">
                <div class="modal-container">
                    <div class="modal-header">
                        <h3>Agregar Venta</h3>
                        <button class="close-modal">&times;</button>
                    </div>
                    <div class="modal-body">
                        <form id="ventaForm">
                            <div class="form-group">
                                <label>RUT comprador</label>
                                <input type="text" id="rut_comprador" required>
                            </div>

                            <div class="form-group">
                                <label>Número de Boleta</label>
                                <input type="text" id="numero_boleta" required>
                            </div>

                            <div class="form-group">
                                <label>Método de pago</label>
                                <input type="text" id="metodo_pago" required>
                            </div>

                            <div class="form-group">
                                <label>Estado</label>
                                <input type="text" id="estado" value="completada" required>
                            </div>

                            <div class="form-group">
                                <label>Farmacia</label>
                                <select id="farmacia" required>
                                    <option value="">Seleccione una farmacia</option>
                                    ${farmacias.map(f => `
                                        <option value="${f.nombre_farmacia}">${f.nombre_farmacia}</option>
                                    `).join('')}
                                </select>
                            </div>

                            <hr>
                            <h4>Detalle de Productos</h4>
                            <div id="detalle-productos-container"></div>
                            <button type="button" class="add-product-btn">+ Agregar Producto</button>

                            <div class="form-actions">
                                <button type="submit" class="submit-btn">Registrar Venta</button>
                                <button type="button" class="cancel-btn">Cancelar</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        document.querySelector('.close-modal').addEventListener('click', closeModal);
        document.querySelector('.cancel-btn').addEventListener('click', closeModal);
        document.getElementById('ventaForm').addEventListener('submit', handleVentaSubmit);

        document.querySelector('.add-product-btn').addEventListener('click', () => addProductoDetalle(productos));
        addProductoDetalle(productos); // Agrega uno por defecto
    } catch (error) {
        alert("Error al cargar formulario: " + error.message);
    }
}

function addProductoDetalle(productos) {
    const container = document.getElementById('detalle-productos-container');
    const index = container.children.length;

    const html = `
        <div class="producto-item" data-index="${index}">
            <label>Producto:</label>
            <select class="producto-select" required>
                <option value="">Seleccione producto</option>
                ${productos.map(p => `
                    <option value="${p.id_producto}" data-nombre="${p.nombre}" data-precio="${p.precio_venta}">
                        ${p.nombre}
                    </option>
                `).join('')}
            </select>

            <label>Cantidad:</label>
            <input type="number" class="cantidad-input" step="1" min="1" required>

            <label>Precio Unitario:</label>
            <input type="number" class="precio-unitario-input" step="0.01" min="0" required>

            <button type="button" class="remove-product-btn">X</button>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', html);

    const addedItem = container.lastElementChild;
    addedItem.querySelector('.remove-product-btn').addEventListener('click', () => addedItem.remove());

    const select = addedItem.querySelector('.producto-select');
    const precioInput = addedItem.querySelector('.precio-unitario-input');

    select.addEventListener('change', () => {
        const selected = select.options[select.selectedIndex];
        precioInput.value = selected.dataset.precio || '';
    });
}

function closeModal() {
    document.querySelector('.modal-overlay')?.remove();
}

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

async function handleVentaSubmit(e) {
    e.preventDefault();
    const submitBtn = document.querySelector('.submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Registrando...';

    const detalles = [];
    const productosDivs = document.querySelectorAll('.producto-item');

    let totalVenta = 0;

    productosDivs.forEach(div => {
        const select = div.querySelector('.producto-select');
        const cantidad = parseFloat(div.querySelector('.cantidad-input').value);
        const precio = parseFloat(div.querySelector('.precio-unitario-input').value);
        const nombre = select.options[select.selectedIndex].text;
        const id_producto = parseInt(select.value);
        const subtotal = cantidad * precio;
        totalVenta += subtotal;

        detalles.push({
            id_producto,
            nombre_producto: nombre,
            cantidad,
            precio_unitario: precio,
            subtotal
        });
    });

    const data = {
        rut_cliente: document.getElementById('rut_comprador').value,
        total_venta: totalVenta,
        metodo_pago: document.getElementById('metodo_pago').value,
        estado_venta: document.getElementById('estado').value,
        farmacia: document.getElementById('farmacia').value,
        numero_boleta: document.getElementById('numero_boleta').value,
        detalles
    };

    try {
        const response = await fetch('http://localhost:8005/realizar/venta/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Error al registrar venta');
        }

        alert('Venta registrada correctamente');
        closeModal();
        // loadVentas(); // opcional
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Registrar Venta';
    }
<<<<<<< HEAD
}
=======
}
>>>>>>> development
