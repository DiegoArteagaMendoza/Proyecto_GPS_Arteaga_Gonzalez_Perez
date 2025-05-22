from rest_framework import serializers
from .models import Rol, Trabajador

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = [
            'id_rol', 'nombre_rol', 'descripcion'
        ]
        read_only_fields = ('id_rol',)

class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = [
            'id_trabajador', 'nombre', 'apellido', 'rut', 'fecha_nacimiento', 'direccion', 'telefono', 'correo_electronico', 'fecha_contratacion', 'estado', 'rol', 'contrasena'
        ]
        read_only_fields = ('id_trabajador',)