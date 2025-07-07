from django.shortcuts import render
from rest_framework.decorators import api_view
from .queryset import UsuarioQuerySet


# Vistas para usuarios
@api_view(['GET'])
def listar_usuarios(request):
    return UsuarioQuerySet.listar_usuarios()
@api_view(['POST'])
def crear_usuario(request):
    return UsuarioQuerySet.crear_usuario(request)


