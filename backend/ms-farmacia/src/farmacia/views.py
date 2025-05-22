from rest_framework.decorators import api_view
from .queryset import FarmaciasQuerySet

@api_view(['GET'])
def listar_farmacias(request):
    return FarmaciasQuerySet.listar_farmacias()

@api_view(['POST'])
def crear_farmacia(request):
    return FarmaciasQuerySet.crear_farmacia(request)