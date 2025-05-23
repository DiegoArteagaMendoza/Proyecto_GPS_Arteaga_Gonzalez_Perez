from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .queryset import VentaQuerySet, BoletaQuerySet

# VENTA
@api_view(['GET'])
def listar_ventas(request):
    return VentaQuerySet.listar_ventas()

@api_view(['GET'])
def listar_venta_ultimos_30_dias(request):
    return VentaQuerySet.listar_venta_ultimos_30_dias()

@api_view(['POST'])
def realizar_venta(request):
    return VentaQuerySet.realizar_venta(request)

@api_view(['GET'])
def listar_venta_por_rut(request):
    return VentaQuerySet.listar_venta_por_rut(request)

#BOLETAS
@api_view(['GET'])
def listar_boletas(request):
    return BoletaQuerySet.listar_boletas()

@api_view(['POST'])
def realizar_boleta(request):
    return BoletaQuerySet.realizar_boleta(request)

@api_view(['GET'])
def listar_boleta_por_rut(request):
    return BoletaQuerySet.listar_boleta_por_rut(request)
