from rest_framework.response import Response
from rest_framework.decorators import api_view
from .queryset import UsuarioQuerySet
from .sistemaCorreos import procesar_envio_recordatorios


# Vistas para usuarios
@api_view(['GET'])
def listar_usuarios(request):
    return UsuarioQuerySet.listar_usuarios()
@api_view(['POST'])
def crear_usuario(request):
    return UsuarioQuerySet.crear_usuario(request)
@api_view(['GET'])
def enviar_recordatorio_vista(request):
    procesar_envio_recordatorios()
    return Response({'mensaje': 'Correos procesados correctamente'})