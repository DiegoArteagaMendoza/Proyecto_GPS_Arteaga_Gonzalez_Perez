from rest_framework import serializers
from .models import Inventario, Producto, Bodega

#Serializer para bodega
class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = [
            'id_bodega', 'nombre', 'farmacia', 'ubicacion', 'estado'
        ]
        read_only_fields = ('id_bodega',)
#serializer para producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id_producto', 'nombre', 'descripcion'
        ]
        read_only_fields = ('id_producto',)


# serializer para inventario
class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = [
            'id_inventario','producto', 'nombre_producto', 'bodega', 'lote', 'fecha_lote', 'fecha_vencimiento', 'cantidad', 'unidad_medida', 'costo_unitario', 'costo_promedio', 'precio_venta', 'stock_minimo'
        ]
        read_only_fields = ('id_inventario',)