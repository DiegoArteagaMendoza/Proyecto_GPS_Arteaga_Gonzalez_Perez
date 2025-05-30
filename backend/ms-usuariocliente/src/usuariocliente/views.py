from django.shortcuts import render
from rest_framework.decorators import api_view
from .queryset import UsuarioQuerySet, FarmaciaQuerySet, productoQuerySet

# Vistas para productos
@api_view(['GET'])
def listar_productos(request):
    return productoQuerySet.listar_productos()

@api_view(['GET'])
def consulta_nombre_producto(request):
    return productoQuerySet.consulta_nombre_producto(request)

# Vista para consultar farmacias donde un producto está disponible
@api_view(['GET'])
def farmacias_con_producto_disponible(request):
    return productoQuerySet.farmacias_con_producto_disponible(request)

# Vistas para usuarios
@api_view(['GET'])
def listar_usuarios(request):
    return UsuarioQuerySet.listar_usuarios()
@api_view(['POST'])
def crear_usuario(request):
    return UsuarioQuerySet.crear_usuario(request)

# Vistas para farmacias
@api_view(['GET'])
def listar_farmacias(request):
    return FarmaciaQuerySet.listar_farmacias()
@api_view(['POST'])
def crear_farmacia(request):
    return FarmaciaQuerySet.crear_farmacia(request)

