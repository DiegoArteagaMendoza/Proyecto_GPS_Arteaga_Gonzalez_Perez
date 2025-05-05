from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .querysets import HolaMundoQuerySet

# Create your views here.
class PruebaView(APIView):
    def get(self, request):
        return HolaMundoQuerySet.consulta_prueba()

    def post(self, request):
        return HolaMundoQuerySet.crear_prueba(request)