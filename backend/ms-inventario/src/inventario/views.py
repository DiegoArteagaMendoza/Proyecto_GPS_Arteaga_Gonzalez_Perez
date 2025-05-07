from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .queryset import InventarioQuerySet, ProdcutosQuerySet
#Vistas para productos

@api_view(['GET'])
def listar_productos(request):
    return ProdcutosQuerySet.listar_productos()

@api_view(['GET'])
def listar_producto_por_nombre(request):
    return ProdcutosQuerySet.listar_producto_por_nombre(request)

@api_view(['GET'])
def consultar_producto_por_id(request):
    return ProdcutosQuerySet.consultar_producto_por_id(request)

@api_view(['POST'])
def crear_producto(request):
    return ProdcutosQuerySet.crear_producto(request)

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

@api_view(['POST'])
def registrar_inventario(request):
    return InventarioQuerySet.crear_inventario(request)