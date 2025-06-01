from django.apps import apps
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioSerializer, FarmaciaSerializer, ProductoSerializer, ProductoFarmaciaSerializer

class UsuarioQuerySet:
    @staticmethod
    def listar_usuarios():
        Usuario = apps.get_model('usuariocliente', 'Usuario')
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def crear_usuario(request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Error al crear usuario", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class productoQuerySet:
    @staticmethod
    def listar_productos():
        Producto = apps.get_model('usuariocliente', 'Producto')
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def consulta_nombre_producto(request):
        Producto = apps.get_model('usuariocliente', 'Producto')
        nombre=request.GET.get('nombre')

        if not nombre:
            return Response({'error':'Debe proporcionar un nombre de producto'}, status=status.HTTP_400_BAD_REQUEST)

        respuesta = Producto.objects.filter(nombre__icontains=nombre)
        serializer = ProductoSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def farmacias_con_producto_disponible(request):
        ProductoFarmacia = apps.get_model('usuariocliente', 'ProductoFarmacia')

        nombre = request.GET.get('nombre')
        if not nombre:
            return Response({'error': 'Debe proporcionar un nombre de producto'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            queryset = ProductoFarmacia.objects.select_related('id_producto', 'id_farmacia').filter(
                id_producto__nombre__icontains=nombre,
                disponible=True,
                stock__gt=0
            )

            serializer = ProductoFarmaciaSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Error en la consulta', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class FarmaciaQuerySet:
    @staticmethod
    def listar_farmacias():
        Farmacia = apps.get_model('usuariocliente', 'Farmacia')
        farmacias = Farmacia.objects.all()
        serializer = FarmaciaSerializer(farmacias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def crear_farmacia(request):
        serializer = FarmaciaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Error al crear farmacia", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
