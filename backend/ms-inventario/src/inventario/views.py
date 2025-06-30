from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .queryset import InventarioQuerySet, ProductosQuerySet, BodegaQuerySet
#Vistas para productos

@api_view(['GET'])
def listar_productos(request):
    return ProductosQuerySet.listar_productos()

@api_view(['GET'])
def listar_producto_por_nombre(request):
    return ProductosQuerySet.listar_producto_por_nombre(request)

@api_view(['GET'])
def consultar_producto_por_id(request):
    return ProductosQuerySet.consultar_producto_por_id(request)

@api_view(['POST'])
def crear_producto(request):
    return ProductosQuerySet.crear_producto(request)

@api_view(['GET'])
def listar_productos_disponibles(request):
    return ProductosQuerySet.listar_productos_disponibles(request)

# Vistas para inventario
@api_view(['GET'])
def obtener_inventario_completo(request):
    return InventarioQuerySet.consultar_inventario_completo()

@api_view(['GET'])
def buscar_inventario_por_nombre_producto(request):
    return InventarioQuerySet.consulta_inventario_nombre_producto(request)

@api_view(['GET'])
def buscar_inventario_por_id_producto(request):
    return InventarioQuerySet.consultar_inventario_por_id_produto(request)

@api_view(['GET'])
def buscar_inventario_por_lote(request):
    return InventarioQuerySet.consulta_inventario_por_lote(request)

@api_view(['GET'])
def obtener_inventario_bajo_stock(request):
    return InventarioQuerySet.consulta_inventario_bajo_stock()

@api_view(['GET'])
def buscar_inventario_por_bodega(request):
    return InventarioQuerySet.consulta_inventario_por_bodega(request)

@api_view(['GET'])
def obtener_disponibilidad_por_farmacia(request):
    return InventarioQuerySet.consultar_inventario_por_farmacia(request)

@api_view(['POST'])
def registrar_inventario(request):
    return InventarioQuerySet.crear_inventario(request)
# Vistas para Bodega
@api_view(['GET'])
def obtener_bodegas(request):
    return BodegaQuerySet.consultar_bodega_completa()

@api_view(['GET'])
def obtener_bodega_por_id(request): 
    return BodegaQuerySet.consultar_bodega_por_id(request)

@api_view(['GET'])
def obtener_bodega_por_nombre(request):
    return BodegaQuerySet.consultar_bodega_por_nombre(request)

@api_view(['GET'])
def obtener_bodega_por_ubicacion(request):
    return BodegaQuerySet.consultar_bodega_por_ubicacion(request)

@api_view(['GET'])
def obtener_bodega_por_estado(request):
    return BodegaQuerySet.consultar_bodega_por_estado(request)

@api_view(['POST'])
def registrar_bodega(request):
    return BodegaQuerySet.crear_bodega(request)
