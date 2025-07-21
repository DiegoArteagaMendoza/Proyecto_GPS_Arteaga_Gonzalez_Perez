from django.apps import apps
from django.db.models import F
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioSerializer

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
    
    @staticmethod
    def usuarios_retiro_24_horas():
        Usuarios = apps.get_model('usuariocliente', 'Usuario')
        usuarios = Usuarios.objects.filter(beneficiario=True).values(
            'nombre',
            'apellido',
            'correo',
            'fecha_registro',
            'medicamentos',
            'retiro_en_dias'
        )
        return usuarios