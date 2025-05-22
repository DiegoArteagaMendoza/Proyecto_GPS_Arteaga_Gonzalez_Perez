from rest_framework import serializers
from .models import Usuario, Farmacia, UsuarioFarmacia, Producto, MedicamentoCliente

# Serializador para la tabla usuarios
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id_usuario', 'rut', 'nombre', 'apellido', 'correo', 'contraseña', 'telefono', 'rol', 'estado', 'fecha_registro'
        ]
        read_only_fields = ('id_usuario',)

# Serializador para la tabla farmacias
class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = [
            'id_farmacia', 'nombre', 'direccion', 'telefono', 'correo', 'estado', 'fecha_registro'
        ]
        read_only_fields = ('id_farmacia',)

# Serializador para la tabla intermedia usuarios_farmacia
class UsuarioFarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioFarmacia
        fields = [
            'id_usuario_farmacia', 'usuario', 'farmacia', 'fecha_asignacion'
        ]
        read_only_fields = ('id_usuario_farmacia',)

# Serializador para la tabla productos
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id_producto', 'nombre', 'descripcion'
        ]
        read_only_fields = ('id_producto',)

# Serializador para la tabla medicamentos_cliente
class MedicamentoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicamentoCliente
        fields = [
            'id_medicamento_cliente', 'usuario', 'producto', 'fecha_asignacion', 'retiro', 'fecha_retiro'
        ]
        read_only_fields = ('id_medicamento_cliente',)