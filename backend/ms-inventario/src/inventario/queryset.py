from django.apps import apps
from django.db import models
from django.db.models import F, Q, Sum
from rest_framework.response import Response
from rest_framework import status
from .serializers import InventarioSerializer, ProductoSerializer, BodegaSerializer

# consultas para Producto
"""
Query set para realizar las consultar referentes al productos
"""
class ProductosQuerySet(models.QuerySet):
    @staticmethod
    def listar_productos():
        Producto = apps.get_model('inventario', 'Producto') #el primero es el nombre de la app y el segundo el nombre del modelo
        respuesta = Producto.objects.all()
        serializer = ProductoSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def listar_producto_por_nombre(request):
        Producto = apps.get_model('inventario', 'Producto')
        nombre_producto = request.GET.get('nombre_producto')
        if not nombre_producto:
            return Response({'error': 'Debe proporcionar un nombre de producto'}, status=status.HTTP_400_BAD_REQUEST)
        respuesta = Producto.objects.filter(nombre__icontains=nombre_producto) 
        serializer = ProductoSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def consultar_producto_por_id(request):
        Producto = apps.get_model('inventario', 'Producto')
        id_producto = request.GET.get('id_producto')
        if not id_producto:
            return Response({'error': 'Debe proporcionar un ID de producto'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            producto = Producto.objects.filter(id_producto=id_producto)
            serializer = ProductoSerializer(producto, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @staticmethod
    def crear_producto(request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error":"error al crear producto", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# consultas para Bodega
"""
Query set para realizar las consultar referentes al bodega
"""
class BodegaQuerySet(models.QuerySet):
    @staticmethod
    def consultar_bodega_completa():
        Bodega = apps.get_model('inventario', 'Bodega')
        respuesta = Bodega.objects.all()
        serializer = BodegaSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def consultar_bodega_por_id(request):
        Bodega = apps.get_model('inventario', 'Bodega')
        id_bodega = request.GET.get('id_bodega')

        if not id_bodega:
            return Response({'error': 'Debe proporcionar un ID de bodega'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bodega = Bodega.objects.filter(id_bodega=id_bodega)
            serializer = BodegaSerializer(bodega, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    def consultar_bodega_por_nombre(request):
        Bodega = apps.get_model('inventario', 'Bodega')
        nombre_bodega = request.GET.get('nombre_bodega')

        if not nombre_bodega:
            return Response({'error': 'Debe proporcionar un nombre de bodega'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bodega = Bodega.objects.filter(nombre__icontains=nombre_bodega)
            serializer = BodegaSerializer(bodega, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def consultar_bodega_por_ubicacion(request):
        Bodega = apps.get_model('inventario', 'Bodega')
        ubicacion_bodega = request.GET.get('ubicacion_bodega')

        if not ubicacion_bodega:
            return Response({'error': 'Debe proporcionar una ubicacion de bodega'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bodega = Bodega.objects.filter(ubicacion__icontains=ubicacion_bodega)
            serializer = BodegaSerializer(bodega, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def consultar_bodega_por_estado(request):
        Bodega = apps.get_model('inventario', 'Bodega')
        estado_bodega = request.GET.get('estado_bodega')

        if not estado_bodega:
            return Response({'error': 'Debe proporcionar un estado de la bodega'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bodega = Bodega.objects.filter(estado=estado_bodega)
            serializer = BodegaSerializer(bodega, many=True)

            data = serializer.data

            for item in data:
                if item.get("estado") == "1.00":
                    item["estado"] = "Activo"
                elif item.get("estado") == "0.00":
                    item["estado"] = "Inactivo"

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    def crear_bodega(request):
        serializer = BodegaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error":"error al guardar bodega", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
    
    # Consultar inventario por farmacia
    @staticmethod
    def consultar_inventario_por_farmacia(request):
        farmacia = request.GET.get('farmacia')
        Inventario = apps.get_model('inventario', 'Inventario')

        inventario = Inventario.objects.filter(bodega__farmacia=farmacia)
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
    
    @staticmethod
    def mostrar_inventario_disponible(request):
        Inventario = apps.get_model('inventario', 'Inventario')
        datos = Inventario.objects.select_related('producto').all()
        resultado = []
        for item in datos:
            resultado.append({
                'nombre_producto': item.nombre_producto,
                'cantidad': item.cantidad,
                'costo_unitario': item.costo_unitario,
                'descripcion': item.producto.descripcion
            })

        return Response(resultado, status=status.HTTP_200_OK)

    # @staticmethod
    # def mostrar_inventario_disponible(request):
    #     Inventario = apps.get_model('inventario', 'Inventario')
    #     query = Inventario.objects.all().values(
    #         nombre_producto = F('nombre_producto'),
    #         cantidad = F('cantidad'),
    #         costo_unitario = F('costo_unitario'),
    #         descripcio = F('producto__descripcion')
    #     )
    #     datos = InventarioQuerySet.mostrar_inventario_disponible(request)
    #     return Response(datos, status=status.HTTP_200_OK)
    
    