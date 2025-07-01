from rest_framework import serializers
from .models import Usuario

# Serializador para la tabla usuarios
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id_usuario', 'rut', 'nombre', 'apellido', 'correo', 'contraseña', 
            'telefono', 'rol', 'estado', 'fecha_registro', 'beneficiario', 
            'medicamentos', 'retiro_en_dias'
        ]
        read_only_fields = ('id_usuario',)