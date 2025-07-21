from rest_framework import serializers
from .models import Venta, DetalleVenta, Boleta
from datetime import datetime, time, timezone
from django.utils.timezone import make_aware, is_naive

# Serializer para Venta
class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = [
            'id_venta', 'fecha_venta', 'rut_cliente', 'total_venta', 
            'metodo_pago', 'estado_venta', 'farmacia'
        ]
        read_only_fields = ('id_venta', 'fecha_venta')

class VentaSerializerDos(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = [
            'id_venta', 'rut_cliente', 'total_venta', 
            'metodo_pago', 'estado_venta', 'farmacia'
        ]
        read_only_fields = ['id_venta']  # Usando lista (estilo más común en DRF)

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        exclude = ['venta']  # La relación se asigna desde el serializer de Venta

class VentaConDetalleSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)
    nombre_cliente = serializers.CharField(write_only=True, required=False)
    numero_boleta = serializers.CharField(write_only=True)

    class Meta:
        model = Venta
        fields = [
            'id_venta', 'fecha_venta', 'rut_cliente', 'total_venta',
            'metodo_pago', 'estado_venta', 'farmacia',
            'detalles', 'nombre_cliente', 'numero_boleta'
        ]
        read_only_fields = ('id_venta', 'fecha_venta')

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        numero_boleta = validated_data.pop('numero_boleta')
        nombre_cliente = validated_data.pop('nombre_cliente', '')

        # Crear la venta
        venta = Venta.objects.create(**validated_data)

        # Crear los detalles de la venta
        for detalle in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle)

        # Crear la boleta asociada
        Boleta.objects.create(
            venta=venta,
            numero_boleta=numero_boleta,
            tipo_documento="boleta",
            total=venta.total_venta,
            rut_cliente=venta.rut_cliente,
            nombre_cliente=nombre_cliente
        )

        return venta


# Serializer para Boleta
class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = [
            'id_boleta', 'venta', 'numero_boleta', 'tipo_documento', 
            'fecha_emision', 'total', 'rut_cliente', 'nombre_cliente'
        ]
        read_only_fields = ('id_boleta', 'fecha_emision')
