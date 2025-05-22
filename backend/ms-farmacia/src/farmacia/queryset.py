from django.apps import apps
from django.db import models
from rest_framework.response import Response
from rest_framework import status
from .serializers import FarmaciaSerializer

"""
Query para farmacias
"""

class FarmaciasQuerySet(models.QuerySet):
    @staticmethod
    def crear_farmacia(request):
        serializer = FarmaciaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def listar_farmacias():
        Farmacias = apps.get_model('farmacia', 'Farmacia')
        respuesta = Farmacias.objects.all()
        serializer = FarmaciaSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)