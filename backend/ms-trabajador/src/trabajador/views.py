from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .queryset import RolesQuerySet, TrabajadorQuerySet, IniciarSesionQuerySet

"""
Vistas para roles
"""
@api_view(['POST'])
def crear_rol(request):
    return RolesQuerySet.crear_rol(request)

@api_view(['GET'])
def listar_roles(request):
    return RolesQuerySet.listar_roles()

"""
Vistas para trabajadores
"""
@api_view(['GET'])
def listar_trabajadores(request):
    return TrabajadorQuerySet.listar_activos(request)

@api_view(['GET'])
def buscar_trabajador_rut(request):
    return TrabajadorQuerySet.buscar_por_rut(request)

@api_view(['GET'])
def buscar_trabajador_nombre(request):
    return TrabajadorQuerySet.buscar_por_nombre(request)

@api_view(['GET'])
def buscar_por_correo(request):
    return TrabajadorQuerySet.buscar_por_correo(request)

@api_view(['PUT'])
def actualizar_trabajador(request):
    return TrabajadorQuerySet.actualizar_trabajador(request)

@api_view(['PUT'])
def desactivar_trabajador(request):
    return TrabajadorQuerySet.desactivar_trabajador(request)

@api_view(['POST'])
def crear_trabajador(request):
    return TrabajadorQuerySet.crear_trabajador(request)

"""
Login
"""
@api_view(['GET'])
def login(request):
    return IniciarSesionQuerySet.login(request)

@api_view(['POST'])
def crear_usuario_cliente(request):
    return IniciarSesionQuerySet.crear_usuario_cliente(request)
