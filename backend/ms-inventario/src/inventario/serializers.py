from rest_framework import serializers
from .models import Inventario,  Producto

# serializer para inventario
class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = [
            'id_inventario','producto', 'nombre_producto', 'bodega', 'lote', 'fecha_lote', 'fecha_vencimiento', 'cantidad', 'unidad_medida', 'costo_unitario', 'costo_promedio', 'precio_venta', 'stock_minimo'
        ]
        read_only_fields = ('id_inventario',)