from django.apps import apps
from django.db import models
from rest_framework.response import Response
from rest_framework import status
from .serializers import PruebaSerializer

class HolaMundoQuerySet(models.QuerySet):

    @staticmethod
    def consulta_prueba():
        Prueba = apps.get_model('holamundo', 'Prueba')

        respuesta = Prueba.objects.all()
        serializer = PruebaSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def crear_prueba(request):
        serializer = PruebaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error":"Error al guardar la prueba", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)