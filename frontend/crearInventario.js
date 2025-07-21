document.getElementById('crearInventario')?.addEventListener('click', openCreateInventarioModal);

async function openCreateInventarioModal() {
    try {
        const productos = await fetchProductos();
        const bodegas = await fetchBodegas();
        const farmacias = await fetchFarmacias();

        const modalHtml = `
            <div class="modal-overlay">
                <div class="modal-container">
                    <div class="modal-header">
                        <h3>Agregar Inventario</h3>
                        <button class="close-modal">&times;</button>
                    </div>
                    <div class="modal-body">
                        <form id="inventarioForm">
                            <div class="form-group">
                                <label>Producto</label>
                                <select id="producto" required>
                                    <option value="">Seleccione un producto</option>
                                    ${productos.map(p => `
                                        <option value="${p.id_producto}">${p.nombre}</option>
                                    `).join('')}
                                </select>
                            </div>

                            <div class="form-group">
                                <label>Nombre del producto</label>
                                <input type="text" id="nombre_producto">
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

                            <div class="form-group">
                                <label>Bodega</label>
                                <select id="bodega" required>
                                    <option value="">Seleccione una bodega</option>
                                    ${bodegas.map(b => `
                                        <option value="${b.id_bodega}">${b.nombre} - ${b.farmacia}</option>
                                    `).join('')}
                                </select>
                            </div>

                            <div class="form-group">
                                <label>Lote</label>
                                <input type="text" id="lote">
                            </div>

                            <div class="form-group">
                                <label>Fecha del Lote</label>
                                <input type="date" id="fecha_lote">
                            </div>

                            <div class="form-group">
                                <label>Fecha de Vencimiento</label>
                                <input type="date" id="fecha_vencimiento">
                            </div>

                            <div class="form-group">
                                <label>Cantidad</label>
                                <input type="number" id="cantidad" step="0.01" min="0">
                            </div>

                            <div class="form-group">
                                <label>Unidad de Medida</label>
                                <input type="text" id="unidad_medida">
                            </div>

                            <div class="form-group">
                                <label>Costo Unitario</label>
                                <input type="number" id="costo_unitario" step="0.0001" min="0">
                            </div>

                            <div class="form-group">
                                <label>Costo Promedio</label>
                                <input type="number" id="costo_promedio" step="0.0001" min="0">
                            </div>

                            <div class="form-group">
                                <label>Precio de Venta</label>
                                <input type="number" id="precio_venta" step="0.0001" min="0">
                            </div>

                            <div class="form-group">
                                <label>Stock Mínimo</label>
                                <input type="number" id="stock_minimo" step="0.01" min="0">
                            </div>

                            <div class="form-actions">
                                <button type="submit" class="submit-btn">Registrar Inventario</button>
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
        document.getElementById('inventarioForm').addEventListener('submit', handleInventarioSubmit);
    } catch (error) {
        alert("Error al cargar formulario: " + error.message);
    }
}

function closeModal() {
    document.querySelector('.modal-overlay')?.remove();
}

async function fetchProductos() {
    const response = await fetch('http://localhost:8002/productos/');
    if (!response.ok) throw new Error("Error al obtener productos");
    return await response.json();
}

async function fetchBodegas() {
    const response = await fetch('http://localhost:8002/bodegas/');
    if (!response.ok) throw new Error("Error al obtener bodegas");
    return await response.json();
}

async function fetchFarmacias() {
    const response = await fetch('http://localhost:8006/farmacias/');
    if (!response.ok) throw new Error("Error al obtener farmacias");
    return await response.json();
}

async function handleInventarioSubmit(e) {
    e.preventDefault();

    const submitBtn = document.querySelector('.submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Registrando...';

    const data = {
        producto: parseInt(document.getElementById('producto').value),
        nombre_producto: (document.getElementById('nombre_producto').value),
        farmacia: (document.getElementById('farmacia').value),
        bodega: parseInt(document.getElementById('bodega').value),
        lote: document.getElementById('lote').value || null,
        fecha_lote: document.getElementById('fecha_lote').value || null,
        fecha_vencimiento: document.getElementById('fecha_vencimiento').value || null,
        cantidad: parseFloat(document.getElementById('cantidad').value) || 0,
        unidad_medida: document.getElementById('unidad_medida').value || null,
        costo_unitario: parseFloat(document.getElementById('costo_unitario').value) || 0,
        costo_promedio: parseFloat(document.getElementById('costo_promedio').value) || 0,
        precio_venta: parseFloat(document.getElementById('precio_venta').value) || 0,
        stock_minimo: parseFloat(document.getElementById('stock_minimo').value) || 0
    };

    console.log("", data);

    try {
        const response = await fetch('http://localhost:8002/inventario/registrar/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Error al registrar inventario');
        }

        alert('Inventario registrado correctamente');
        closeModal();
        // Aquí puedes volver a cargar la tabla de inventario si tienes una función como loadInventarios()
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Registrar Inventario';
    }
}
