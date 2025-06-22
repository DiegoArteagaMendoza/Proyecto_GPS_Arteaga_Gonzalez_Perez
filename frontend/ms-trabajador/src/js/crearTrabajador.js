document.addEventListener('DOMContentLoaded', async function () {
    // Fetch roles when page loads
    try {
        const roles = await fetchRoles();
        populateRoleDropdown(roles);
    } catch (error) {
        console.error('Error loading roles:', error);
        showAlert('Error al cargar los roles. Por favor recargue la página.', 'error');
    }

    // Form submission handler
    document.getElementById('employeeForm').addEventListener('submit', async function (e) {
        e.preventDefault();

        // Get the selected role text (nombre_rol) instead of ID
        const roleSelect = document.getElementById('role');
        const selectedRole = roleSelect.options[roleSelect.selectedIndex].text;

        // Get form values and map to model fields
        const employeeData = {
            nombre: document.getElementById('firstName').value.trim(),
            apellido: document.getElementById('lastName').value.trim(),
            rut: document.getElementById('rut').value,
            fecha_nacimiento: document.getElementById('dob').value,
            direccion: document.getElementById('address').value.trim(),
            telefono: document.getElementById('phone').value.trim(),
            correo_electronico: document.getElementById('email').value.trim(),
            estado: document.getElementById('active').checked,
            rol: selectedRole,  // Send the role name (nombre_rol) instead of ID
            contrasena: document.getElementById('password').value
        };

        // Validate form
        if (!validateEmployeeForm(employeeData)) {
            return;
        }

        try {
            // Show loading state
            const submitBtn = document.querySelector('.submit-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Registrando...';

            // Send data to the endpoint
            const response = await fetch('https://ms-trabajador-production.up.railway.app/trabajador/registrar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(employeeData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Error al registrar el trabajador');
            }

            const result = await response.json();

            // Show success message
            showAlert('Trabajador registrado exitosamente!', 'success');

            // Reset the form
            document.getElementById('employeeForm').reset();

        } catch (error) {
            console.error('Error:', error);
            showAlert(error.message || 'Hubo un error al registrar el trabajador. Por favor intente nuevamente.', 'error');
        } finally {
            // Reset button state
            const submitBtn = document.querySelector('.submit-btn');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Registrar Trabajador';
        }
    });

    // RUT formatting
    document.getElementById('rut').addEventListener('input', function (e) {
        formatRUT(e.target);
    });
});

/**
 * Fetches roles from API
 */
async function fetchRoles() {
    const response = await fetch('http://ms-trabajador-production-f278.up.railway.app/roles/');
    if (!response.ok) {
        throw new Error('Error al obtener los roles');
    }
    return await response.json();
}

/**
 * Populates the role dropdown with fetched roles
 */
function populateRoleDropdown(roles) {
    const roleSelect = document.getElementById('role');

    // Clear existing options except the first one
    while (roleSelect.options.length > 1) {
        roleSelect.remove(1);
    }

    // Add new options
    roles.forEach(role => {
        const option = document.createElement('option');
        option.value = role.id_rol;  // Store ID in value
        option.textContent = role.nombre_rol;  // Show role name in dropdown
        roleSelect.appendChild(option);
    });
}

/**
 * Validates employee form data
 */
function validateEmployeeForm(data) {
    // Required fields
    if (!data.nombre) {
        showAlert('Por favor ingrese el nombre', 'error');
        return false;
    }

    if (!data.apellido) {
        showAlert('Por favor ingrese el apellido', 'error');
        return false;
    }

    if (!data.rut) {
        showAlert('Por favor ingrese el RUT', 'error');
        return false;
    }

    if (!validateRUT(data.rut)) {
        showAlert('El RUT ingresado no es válido', 'error');
        return false;
    }

    if (!data.rol || data.rol === "Seleccione un rol") {
        showAlert('Por favor seleccione un rol', 'error');
        return false;
    }

    if (!data.contrasena || data.contrasena.length < 6) {
        showAlert('La contraseña debe tener al menos 6 caracteres', 'error');
        return false;
    }

    if (data.correo_electronico && !validateEmail(data.correo_electronico)) {
        showAlert('El correo electrónico no es válido', 'error');
        return false;
    }

    return true;
}

/**
 * Formats RUT input (XX.XXX.XXX-X)
 */
function formatRUT(input) {
    let rut = input.value.replace(/\./g, '').replace(/\-/g, '').toUpperCase();

    if (rut.length > 1) {
        const dv = rut.slice(-1);
        const body = rut.slice(0, -1);
        const formattedBody = body.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        input.value = `${formattedBody}-${dv}`;
    } else {
        input.value = rut;
    }
}

/**
 * Validates Chilean RUT
 */
function validateRUT(rut) {
    // First remove formatting for validation
    rut = rut.replace(/\./g, '').replace(/\-/g, '').toUpperCase();

    if (rut.length < 2) return false;

    const body = rut.slice(0, -1);
    const dv = rut.slice(-1);

    if (!/^\d+$/.test(body)) return false;

    let sum = 0;
    let multiplier = 2;

    for (let i = body.length - 1; i >= 0; i--) {
        sum += parseInt(body.charAt(i)) * multiplier;
        multiplier = multiplier === 7 ? 2 : multiplier + 1;
    }

    const expectedDV = 11 - (sum % 11);
    let calculatedDV;

    if (expectedDV === 11) calculatedDV = '0';
    else if (expectedDV === 10) calculatedDV = 'K';
    else calculatedDV = expectedDV.toString();

    return calculatedDV === dv;
}

/**
 * Validates email format
 */
function validateEmail(email) {
    if (!email) return true; // Optional field
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
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
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}