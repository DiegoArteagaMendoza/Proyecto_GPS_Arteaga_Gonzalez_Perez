document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('usuarioForm');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const data = {
            rut: document.getElementById('rut').value.trim(),
            nombre: document.getElementById('nombre').value.trim(),
            apellido: document.getElementById('apellido').value.trim(),
            correo: document.getElementById('correo').value.trim(),
            contraseña: document.getElementById('contrasena').value,
            telefono: document.getElementById('telefono').value.trim() || null,
            rol: "cliente"
        };

        try {
            const response = await fetch('https://ms-usuariocliente-production.up.railway.app/usuarios/registrar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.message || 'Error al registrar el usuario');
            }

            alert('Usuario registrado correctamente');
            form.reset();
        } catch (error) {
            console.error('Error:', error);
            alert(error.message || 'Error al registrar el usuario');
        }
    });
});
