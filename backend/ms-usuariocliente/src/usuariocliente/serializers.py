from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    fecha_registro = serializers.SerializerMethodField()

    def get_fecha_registro(self, obj):
        # Convierte datetime a date y a string, si es necesario
        if hasattr(obj.fecha_registro, 'date'):
            return obj.fecha_registro.date().isoformat()
        return obj.fecha_registro  # ya es date

    class Meta:
        model = Usuario
        fields = [
            'id_usuario', 'rut', 'nombre', 'apellido', 'correo', 'contraseña',
            'telefono', 'rol', 'estado', 'fecha_registro', 'beneficiario',
            'medicamentos', 'retiro_en_dias'
        ]
        read_only_fields = ('id_usuario',)

class UsuarioRetiroMedicamentos(serializers.Serializer):
    nombre = serializers.CharField()
    apellido = serializers.CharField()
    correo = serializers.EmailField()
    fecha_registro = serializers.DateField()
    medicamentos = serializers.CharField()
    retiro_en_dias = serializers.IntegerField()

    class Meta:
        model = Usuario
        fields = (
            'nombre',
            'apellido',
            'correo',
            'fecha_registro',
            'medicamentos',
            'retiro_en_dias'
        )