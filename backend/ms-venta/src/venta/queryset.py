from django.apps import apps
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import VentaSerializer, DetalleVentaSerializer, BoletaSerializer
#CONSULTAS VENTA
class VentaQuerySet(models.QuerySet):
    @staticmethod
    def listar_ventas():
        Venta = apps.get_model('venta', 'Venta')
        respuesta = Venta.objects.all()
        serializer = VentaSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def listar_venta_ultimos_30_dias():
        Venta = apps.get_model('venta', 'Venta')
        hace_30_dias = timezone.now() - timedelta(days=30)
        ventas = Venta.objects.filter(fecha_venta__gte=hace_30_dias)
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def realizar_venta(request):
        serializer = VentaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error":"error al crear/realizar la venta", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def listar_venta_por_rut(request):
        Venta = apps.get_model('venta', 'Venta')
        rut_cliente = request.GET.get('rut_cliente')
        if not rut_cliente:
            return Response({'error': 'Debe proporcionar un rut'}, status=status.HTTP_400_BAD_REQUEST)
        respuesta = Venta.objects.filter(rut__icontains=rut_cliente)
        serializer = VentaSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#CONSULTAS DETALLE DE VENTA
#que se genere automaticamente al realizar una venta con la info 
#del producto, la tabla venta y la boleta
class DetalleVentaQuerySet(models.QuerySet):
    @staticmethod
    def listar_detalle_ventas():
        DetalleVenta = apps.get_model('venta', 'DetalleVenta')
        respuesta = DetalleVenta.objects.all()
        serializer = DetalleVentaSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#CONSULTAS BOLETA

class BoletaQuerySet(models.QuerySet):
    @staticmethod
    def listar_boletas():
        Boleta = apps.get_model('venta', 'Boleta')
        respuesta = Boleta.objects.all()
        serializer = BoletaSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @staticmethod
    def realizar_boleta(request):
        Venta = apps.get_model('venta', 'Venta')
        Boleta = apps.get_model('venta', 'Boleta')
        id_venta = request.data.get("id_venta")
        numero_boleta = request.data.get("numero_boleta")
        tipo_documento = request.data.get("tipo_documento", "boleta")  
        nombre_cliente = request.data.get("nombre_cliente", "")  

        if not id_venta:
            return Response({"error": "Debe proporcionar el id_venta"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            venta = Venta.objects.get(id_venta=id_venta)
        except Venta.DoesNotExist:
            return Response({"error": "La venta no existe"}, status=status.HTTP_404_NOT_FOUND)

        try:
            boleta = Boleta.objects.create(
                venta=venta,
                numero_boleta=numero_boleta,
                tipo_documento=tipo_documento,
                total=venta.total_venta,
                rut_cliente=venta.rut_cliente,
                nombre_cliente=nombre_cliente
            )
            serializer = BoletaSerializer(boleta)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Error al crear la boleta", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # serializer = BoletaSerializer(data=request.data)
        # if serializer.is_valid():
        #     try:
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     except Exception as e:
        #         return Response({"error":"error al crear/realizar la boleta", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def listar_boleta_por_rut(request):
        Boleta = apps.get_model('venta', 'Boleta')
        rut_cliente = request.GET.get('rut_cliente')
        if not rut_cliente:
            return Response({'error': 'Debe proporcionar un rut'}, status=status.HTTP_400_BAD_REQUEST)
        respuesta = Boleta.objects.filter(rut_cliente__icontains=rut_cliente)
        serializer = BoletaSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

