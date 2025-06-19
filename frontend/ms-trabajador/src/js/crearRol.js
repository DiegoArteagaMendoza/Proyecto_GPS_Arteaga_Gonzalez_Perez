document.addEventListener('DOMContentLoaded', function () {
    const roleForm = document.getElementById('roleForm');

    roleForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Get form values
        const roleData = {
            nombre_rol: document.getElementById('nombreRol').value.trim(),
            descripcion: document.getElementById('descripcion').value.trim() || null
        };

        // Validate form
        if (!validateForm(roleData)) {
            return;
        }

        try {
            // Show loading state
            const submitBtn = document.querySelector('.submit-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Creando...';

            // Send data to the endpoint
            const response = await fetch('https://ms-trabajador-production-f278.up.railway.app/roles/crear/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(roleData)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.message || 'Error en el servidor');
            }

            // Show success message
            showAlert('Rol creado exitosamente!', 'success');

            // Reset the form
            roleForm.reset();

        } catch (error) {
            console.error('Error:', error);
            showAlert(error.message || 'Error al crear el rol', 'error');

            // Handle duplicate role name error
            if (error.message.includes('nombre_rol')) {
                document.getElementById('nombreRolError').textContent = 'Este nombre de rol ya existe';
                document.getElementById('nombreRolError').style.display = 'block';
            }
        } finally {
            // Reset button state
            const submitBtn = document.querySelector('.submit-btn');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Crear Rol';
        }
    });

    // Clear error when typing
    document.getElementById('nombreRol').addEventListener('input', function () {
        document.getElementById('nombreRolError').style.display = 'none';
    });
});

/**
 * Validates the role form data
 */
function validateForm(data) {
    // Clear previous errors
    document.getElementById('nombreRolError').style.display = 'none';

    // Required field validation
    if (!data.nombre_rol) {
        document.getElementById('nombreRolError').textContent = 'El nombre del rol es requerido';
        document.getElementById('nombreRolError').style.display = 'block';
        return false;
    }

    // Name length validation
    if (data.nombre_rol.length > 255) {
        document.getElementById('nombreRolError').textContent = 'El nombre no puede exceder 255 caracteres';
        document.getElementById('nombreRolError').style.display = 'block';
        return false;
    }

    return true;
}

/**
 * Shows alert message
 */
function showAlert(message, type = 'error') {
    // Remove existing alerts
    const existingAlert = document.querySelector('.alert');
    if (existingAlert) {
        existingAlert.remove();
    }

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    // Insert after the title
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.querySelector('form'));

    // Auto-remove after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}