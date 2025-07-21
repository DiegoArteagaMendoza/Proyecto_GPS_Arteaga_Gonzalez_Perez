 let medicamentosDisponibles = [];
let medicamentosSeleccionados = [];

// Función para alternar la sección de medicamentos
function toggleMedicamentos() {
    const beneficiario = document.getElementById('beneficiario').checked;
    const medicamentosSection = document.getElementById('medicamentos-section');
    
    if (beneficiario) {
        medicamentosSection.classList.add('active');
        cargarMedicamentos();
    } else {
        medicamentosSection.classList.remove('active');
        medicamentosSeleccionados = [];
        actualizarMedicamentosSeleccionados();
    }
}

// Función para cargar medicamentos del inventario
async function cargarMedicamentos() {
    const loading = document.getElementById('loading');
    const content = document.getElementById('medicamentos-content');
    
    loading.classList.add('active');
    content.style.display = 'none';

    try {
        // URL CORREGIDA: cambiada de /inventario/ a /productos/
        const response = await fetch('https://ms-inventario-production-98de.up.railway.app/productos/');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        medicamentosDisponibles = data;
        
        console.log('Productos cargados:', medicamentosDisponibles);
        
        mostrarMedicamentos(medicamentosDisponibles);
        
        loading.classList.remove('active');
        content.style.display = 'block';
        
    } catch (error) {
        console.error('Error cargando productos:', error);
        loading.innerHTML = `
            <p style="color: #d32f2f;">❌ Error al cargar productos del inventario</p>
            <p style="font-size: 14px; color: #666;">
                Verifica que el microservicio de inventario esté ejecutándose en 
                <strong>https://ms-inventario-production-98de.up.railway.app/productos/</strong>
            </p>
            <p style="font-size: 12px; color: #999; margin-top: 10px;">
                Error técnico: ${error.message}
            </p>
        `;
    }
}

// Función para mostrar medicamentos en la grilla
function mostrarMedicamentos(medicamentos) {
    const grid = document.getElementById('medicamentos-grid');
    
    if (!medicamentos || medicamentos.length === 0) {
        grid.innerHTML = '<p style="text-align: center; color: #666; grid-column: span 2;">No hay productos disponibles</p>';
        return;
    }

    grid.innerHTML = medicamentos.map(medicamento => {
        // Adaptar a diferentes estructuras de respuesta del API
        const id = medicamento.id || medicamento.id_producto || medicamento.pk;
        const nombre = medicamento.nombre || medicamento.nombre_producto || medicamento.producto || 'Sin nombre';
        const categoria = medicamento.categoria || medicamento.tipo || medicamento.clasificacion || 'Sin categoría';
        const stock = medicamento.stock || medicamento.cantidad || medicamento.existencia || 0;
        const precio = medicamento.precio || medicamento.valor || medicamento.costo || 0;

        return `
            <div class="medicamento-item" onclick="toggleMedicamento(${id})">
                <input type="checkbox" 
                       id="med-${id}" 
                       ${medicamentosSeleccionados.some(m => (m.id || m.id_producto || m.pk) === id) ? 'checked' : ''}
                       onchange="toggleMedicamento(${id})" 
                       onclick="event.stopPropagation()">
                <div class="medicamento-info">
                    <div class="medicamento-nombre">${nombre}</div>
                    <div class="medicamento-detalles">
                        ${categoria} • 
                        Stock: ${stock} • 
                        $${precio}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Función para alternar selección de medicamento
function toggleMedicamento(id) {
    const medicamento = medicamentosDisponibles.find(m => (m.id || m.id_producto || m.pk) === id);
    const checkbox = document.getElementById(`med-${id}`);
    
    if (!medicamento) {
        console.warn(`Producto con ID ${id} no encontrado`);
        return;
    }

    const productoId = medicamento.id || medicamento.id_producto || medicamento.pk;
    const index = medicamentosSeleccionados.findIndex(m => (m.id || m.id_producto || m.pk) === productoId);
    
    if (index === -1) {
        medicamentosSeleccionados.push(medicamento);
        if (checkbox) checkbox.checked = true;
    } else {
        medicamentosSeleccionados.splice(index, 1);
        if (checkbox) checkbox.checked = false;
    }
    
    actualizarMedicamentosSeleccionados();
}

// Función para actualizar la vista de medicamentos seleccionados
function actualizarMedicamentosSeleccionados() {
    const container = document.getElementById('medicamentos-seleccionados');
    const contador = document.getElementById('contador-medicamentos');
    const tags = document.getElementById('medicamentos-tags');
    
    contador.textContent = medicamentosSeleccionados.length;
    
    if (medicamentosSeleccionados.length === 0) {
        container.style.display = 'none';
        return;
    }
    
    container.style.display = 'block';
    tags.innerHTML = medicamentosSeleccionados.map(medicamento => {
        const id = medicamento.id || medicamento.id_producto || medicamento.pk;
        const nombre = medicamento.nombre || medicamento.nombre_producto || medicamento.producto || 'Sin nombre';
        
        return `
            <div class="medicamento-tag">
                ${nombre}
                <span class="remove" onclick="toggleMedicamento(${id})">×</span>
            </div>
        `;
    }).join('');
}

// Función para filtrar medicamentos
function filtrarMedicamentos() {
    const searchTerm = document.getElementById('search-medicamentos').value.toLowerCase();
    const medicamentosFiltrados = medicamentosDisponibles.filter(medicamento => {
        const nombre = (medicamento.nombre || medicamento.nombre_producto || medicamento.producto || '').toLowerCase();
        const categoria = (medicamento.categoria || medicamento.tipo || medicamento.clasificacion || '').toLowerCase();
        
        return nombre.includes(searchTerm) || categoria.includes(searchTerm);
    });
    
    mostrarMedicamentos(medicamentosFiltrados);
}

// Función para crear usuario cliente
async function crearUsuarioCliente() {
    // Validar campos obligatorios
    const rut = document.getElementById('rut').value.trim();
    const nombre = document.getElementById('nombre').value.trim();
    const apellido = document.getElementById('apellido').value.trim();
    const correo = document.getElementById('correo').value.trim();
    const contrasena = document.getElementById('contrasena').value.trim();
    const beneficiario = document.getElementById('beneficiario').checked;
    const retiro = document.getElementById('retiro').value.trim();

    if (!rut || !nombre || !apellido || !correo || !contrasena) {
        mostrarMensaje('Por favor complete todos los campos obligatorios', 'error');
        return;
    }

    if (beneficiario && medicamentosSeleccionados.length === 0) {
        mostrarMensaje('Los beneficiarios deben tener al menos un medicamento seleccionado', 'error');
        return;
    }

    const formData = {
        rut: rut,
        nombre: nombre,
        apellido: apellido,
        correo: correo,
        contraseña: contrasena,
        telefono: document.getElementById('telefono').value.trim(),
        rol: "cliente",
        beneficiario: beneficiario,
        retiro_en_dias: retiro
    };

    // Si es beneficiario, agregar medicamentos
    if (beneficiario) {
        const medicamentosNombres = medicamentosSeleccionados.map(m => 
            m.nombre || m.nombre_producto || m.producto || 'Sin nombre'
        );
        formData.medicamentos = medicamentosNombres.join('; ');
    }

    try {
        const response = await fetch('https://ms-trabajador-production.up.railway.app/usuario/crear-cliente/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            mostrarMensaje('Usuario creado exitosamente', 'success');
            mostrarUsuarioCreado(data);
            limpiarFormulario();
        } else {
            mostrarMensaje('Error: ' + (data.error || 'Error desconocido'), 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarMensaje('Error de conexión con el servidor', 'error');
    }
}

// Función para mostrar mensajes
function mostrarMensaje(mensaje, tipo) {
    const resultado = document.getElementById('resultado');
    resultado.className = `resultado show ${tipo === 'error' ? 'error-message' : 'success-message'}`;
    resultado.innerHTML = `<p>${mensaje}</p>`;
    
    setTimeout(() => {
        if (tipo === 'error') {
            resultado.classList.remove('show');
        }
    }, 5000);
}

// Función para mostrar usuario creado
function mostrarUsuarioCreado(usuario) {
    let html = `
        <div class="usuario-creado">
            <h3>✅ Usuario Creado Exitosamente</h3>
            <p><strong>RUT:</strong> ${usuario.rut}</p>
            <p><strong>Nombre:</strong> ${usuario.nombre} ${usuario.apellido}</p>
            <p><strong>Correo:</strong> ${usuario.correo}</p>
            <p><strong>Teléfono:</strong> ${usuario.telefono || 'No especificado'}</p>
            <p><strong>Rol:</strong> ${usuario.rol}</p>
            <p><strong>Beneficiario:</strong> ${usuario.beneficiario ? 'Sí' : 'No'}</p>
    `;

    if (usuario.beneficiario && usuario.medicamentos_lista && usuario.medicamentos_lista.length > 0) {
        html += `
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
                <h4>💊 Medicamentos Asignados (${usuario.total_medicamentos || usuario.medicamentos_lista.length})</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
        `;
        
        usuario.medicamentos_lista.forEach(medicamento => {
            html += `<span style="background: #4CAF50; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px;">${medicamento}</span>`;
        });
        
        html += `</div></div>`;
    }

    html += `</div>`;
    
    const resultado = document.getElementById('resultado');
    resultado.innerHTML = html;
}

// Función para limpiar formulario
function limpiarFormulario() {
    document.getElementById('usuarioForm').reset();
    medicamentosSeleccionados = [];
    document.getElementById('medicamentos-section').classList.remove('active');
    actualizarMedicamentosSeleccionados();
}

// Inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema de gestión de clientes cargado');
    console.log('URL del microservicio de inventario: https://ms-inventario-production-98de.up.railway.app/productos/');
});