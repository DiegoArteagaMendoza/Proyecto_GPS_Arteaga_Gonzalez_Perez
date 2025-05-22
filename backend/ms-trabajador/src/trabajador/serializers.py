from rest_framework import serializers
from .models import Rol, Trabajador, AsignacionRol

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
            'id_trabajador', 'nombre', 'apellido', 'rut', 'fecha_nacimiento', 'direccion', 'telefono', 'correo_electronico', 'fecha_contratacion', 'estado', 'id_departamento'
        ]
        read_only_fields = ('id_trabajador',)

class AsignacionRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignacionRol
        fields = [
            'id_trabajador', 'id_rol', 'fecha_inicio', 'fecha_fin', 'activo'
        ]
        read_only_fields = ('id_trabajador', 'id_rol',)