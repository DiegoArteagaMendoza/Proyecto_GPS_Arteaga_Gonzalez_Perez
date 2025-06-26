from rest_framework import serializers
from .models import Usuario, Farmacia, UsuarioFarmacia, Producto, MedicamentoCliente, ProductoFarmacia

# Serializador para la tabla usuarios
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id_usuario', 'rut', 'nombre', 'apellido', 'correo', 'contraseña', 'telefono', 'rol', 'estado', 'fecha_registro'
        ]
        read_only_fields = ('id_usuario',)