from django.apps import apps
from django.db import models
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import InventarioSerializer, ProductoSerializer, BodegaSerializer, MovimientoInventarioSerializer

# consultas para producto
"""
Query set para realizar las consultar referentes a producto
"""
class ProdcutosQuerySet(models.QuerySet):
    # Consulta todos los productos
    @staticmethod
    def consultar_productos():
        Producto = apps.get_model('inventario', 'Producto')
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Consultar producto por nombre (búsqueda parcial)
    @staticmethod
    def consulta_producto_por_nombre(request):
        Producto = apps.get_model('inventario', 'Producto')
        nombre = request.query_params.get('nombre')

        if not nombre:
            return Response({'error': 'Debe proporcionar un nombre de producto'}, status=status.HTTP_400_BAD_REQUEST)

        productos = Producto.objects.filter(nombre__icontains=nombre)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Consultar producto por id_producto
    @staticmethod
    def consulta_producto_por_id(request):
        Producto = apps.get_model('inventario', 'Producto')
        id_producto = request.query_params.get('id_producto')

        if not id_producto:
            return Response({'error': 'Debe proporcionar un ID de producto'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            producto = Producto.objects.get(id_producto=id_producto)
            serializer = ProductoSerializer(producto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Crear nuevo producto
    @staticmethod
    def crear_producto(request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Error al guardar el producto", "detalle": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# consultas para bodega
"""
Query set para realizar las consultar referentes a bodega
"""
class BodegaQuerySet(models.QuerySet):
    # Consultar todas las bodegas
    @staticmethod
    def listar_bodegas():
        Bodega = apps.get_model('inventario', 'Bodega')
        bodegas = Bodega.objects.all()
        serializer = BodegaSerializer(bodegas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Buscar bodegas por nombre (búsqueda parcial)
    @staticmethod
    def buscar_bodega_por_nombre(request):
        Bodega = apps.get_model('inventario', 'Bodega')
        nombre = request.query_params.get('nombre')

        if not nombre:
            return Response({'error': 'Debe proporcionar un nombre de bodega'}, status=status.HTTP_400_BAD_REQUEST)

        bodegas = Bodega.objects.filter(nombre__icontains=nombre)
        serializer = BodegaSerializer(bodegas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Buscar bodega por id_bodega
    @staticmethod
    def buscar_bodega_por_id(request):
        Bodega = apps.get_model('inventario', 'Bodega')
        id_bodega = request.query_params.get('id_bodega')

        if not id_bodega:
            return Response({'error': 'Debe proporcionar un ID de bodega'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bodega = Bodega.objects.get(id_bodega=id_bodega)
            serializer = BodegaSerializer(bodega)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Bodega.DoesNotExist:
            return Response({'error': 'Bodega no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    # Crear nueva bodega (opcional, si permites escritura)
    @staticmethod
    def crear_bodega(request):
        serializer = BodegaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Error al guardar la bodega", "detalle": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


        
# consultas para movimientos inventario
class MovimientoInventarioQuerySet(models.QuerySet):
# Listar todos los movimientos
    @staticmethod
    def listar_movimientos():
        MovimientoInventario = apps.get_model('inventario', 'MovimientoInventario')
        movimientos = MovimientoInventario.objects.all().select_related('inventario', 'inventario__producto')
        serializer = MovimientoInventarioSerializer(movimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Buscar movimiento por ID
    @staticmethod
    def buscar_movimiento_por_id(request):
        MovimientoInventario = apps.get_model('inventario', 'MovimientoInventario')
        id_movimiento = request.query_params.get('id_movimiento')

        if not id_movimiento:
            return Response({'error': 'Debe proporcionar un ID de movimiento'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movimiento = MovimientoInventario.objects.select_related('inventario', 'inventario__producto').get(id_movimiento=id_movimiento)
            serializer = MovimientoInventarioSerializer(movimiento)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MovimientoInventario.DoesNotExist:
            return Response({'error': 'Movimiento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Buscar movimientos por tipo (entrada/salida)
    @staticmethod
    def buscar_movimiento_por_tipo(request):
        MovimientoInventario = apps.get_model('inventario', 'MovimientoInventario')
        tipo = request.query_params.get('tipo_movimiento')

        if tipo not in ['entrada', 'salida']:
            return Response({'error': 'Tipo de movimiento inválido. Debe ser "entrada" o "salida"'}, status=status.HTTP_400_BAD_REQUEST)

        movimientos = MovimientoInventario.objects.filter(tipo_movimiento=tipo).select_related('inventario', 'inventario__producto')
        serializer = MovimientoInventarioSerializer(movimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Buscar movimientos por rango de fechas
    @staticmethod
    def buscar_movimiento_por_fecha(request):
        MovimientoInventario = apps.get_model('inventario', 'MovimientoInventario')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe proporcionar una fecha de inicio y una fecha de fin'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from django.utils.dateparse import parse_datetime
            fecha_inicio = parse_datetime(fecha_inicio)
            fecha_fin = parse_datetime(fecha_fin)
            if not fecha_inicio or not fecha_fin:
                raise ValueError("Formato de fecha inválido")
        except Exception:
            return Response({'error': 'Formato de fecha inválido. Use formato ISO 8601 (ej. 2025-05-01T10:00:00)'}, status=status.HTTP_400_BAD_REQUEST)

        movimientos = MovimientoInventario.objects.filter(
            fecha_movimiento__range=(fecha_inicio, fecha_fin)
        ).select_related('inventario', 'inventario__producto')

        serializer = MovimientoInventarioSerializer(movimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Crear un nuevo movimiento
    @staticmethod
    def crear_movimiento(request):
        serializer = MovimientoInventarioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Error al guardar el movimiento", "detalle": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)