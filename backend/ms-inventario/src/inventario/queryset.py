from django.apps import apps
from django.db import models
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import InventarioSerializer, ProductoSerializer

# consultas para inventario
"""
Query set para realizar las consultar referentes al productos
"""


# consultas para inventario
"""
Query set para realizar las consultar referentes al bodega
"""


# consultas para inventario
"""
Query set para realizar las consultar referentes al inventario
"""
class InventarioQuerySet(models.QuerySet):
    
    # consulta de inventario completo
    @staticmethod
    def consultar_inventario_completo():
        Inventario = apps.get_model('inventario', 'Inventario')

        respuesta = Inventario.objects.all()
        serializer = InventarioSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # consultar de inventario mediante nombre_producto
    @staticmethod
    def consulta_inventario_nombre_producto(request):
        Inventario = apps.get_model('inventario', 'Inventario')
        nombre_producto=request.GET.get('nombre_producto')

        if not nombre_producto:
            return Response({'error':'Debe proporcionar un nombre de producto'}, status=status.HTTP_400_BAD_REQUEST)

        respuesta = Inventario.objects.filter(nombre_producto__icontains=nombre_producto)
        serializer = InventarioSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Consultar por id_producto
    @staticmethod
    def consultar_inventario_por_id_produto(request):
        Inventario = apps.get_model('inventario', 'Inventario')
        id_producto = request.GET.get('id_producto')

        if not id_producto:
            return Response({'error': 'Debe proporcionar un ID de producto'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            inventario = Inventario.objects.filter(producto__id_producto=id_producto)
            serializer = InventarioSerializer(inventario, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Consultar por lote
    @staticmethod
    def consulta_inventario_por_lote(request):
        lote = request.GET.get('lote')
        Inventario = apps.get_model('inventario', 'Inventario')
        
        inventario = Inventario.objects.filter(lote=lote)
        serializer = InventarioSerializer(inventario, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Consultar productos con stock bajo (menos que stock_minimo)
    @staticmethod
    def consulta_inventario_bajo_stock():
        Inventario = apps.get_model('inventario', 'Inventario')
        
        inventario = Inventario.objects.filter(cantidad__lt=models.F('stock_minimo'))
        serializer = InventarioSerializer(inventario, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Consultar inventario por bodega
    @staticmethod
    def consulta_inventario_por_bodega(request):
        id_bodega = request.GET.get('id_bodega')
        Inventario = apps.get_model('inventario', 'Inventario')
        
        inventario = Inventario.objects.filter(bodega__id_bodega=id_bodega)
        serializer = InventarioSerializer(inventario, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Crear inventario
    @staticmethod
    def crear_inventario(request):
        serializer = InventarioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error":"error al guardar inventario", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)