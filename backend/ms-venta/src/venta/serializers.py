from rest_framework import serializers
from .models import Venta, DetalleVenta, Boleta

# Serializer para Venta
class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = [
            'id_venta', 'fecha_venta', 'rut_cliente', 'total_venta', 
            'metodo_pago', 'estado_venta', 'farmacia'
        ]
        read_only_fields = ('id_venta', 'fecha_venta')


# Serializer para DetalleVenta
class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = [
            'id_detalle', 'venta', 'id_producto', 'nombre_producto', 
            'cantidad', 'precio_unitario', 'subtotal'
        ]
        read_only_fields = ('id_detalle',)


# Serializer para Boleta
class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = [
            'id_boleta', 'venta', 'numero_boleta', 'tipo_documento', 
            'fecha_emision', 'total', 'rut_cliente', 'nombre_cliente'
        ]
        read_only_fields = ('id_boleta', 'fecha_emision')
