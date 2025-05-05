from rest_framework.views import APIView
from .querysets import HolaMundoQuerySet


# Create your views here.
class PruebaView(APIView):
    def get(self,request):
        return HolaMundoQuerySet.consultaPrueba()
    
    def post(self, request):
        return HolaMundoQuerySet.crearPrueba(request)
    