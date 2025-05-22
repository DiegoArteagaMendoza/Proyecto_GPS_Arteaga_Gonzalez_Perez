from django.apps import apps
from django.db import models
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import RolSerializer, TrabajadorSerializer, AsignacionRolSerializer
   
"""
Querys para roles
"""
class RolesQuerySet(models.QuerySet):
    @staticmethod
    def crear_rol(request):
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error":"error al crear un rol", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def listar_roles():
        Rol = apps.get_model('trabajador', 'Rol')    
        respuesta = Rol.objects.all()
        serializer = RolSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
"""
Query para trabajadores
"""
class TrabajadorQuerySet(models.QuerySet):
    @staticmethod
    def crear_trabajador(request):
        serializer = TrabajadorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error":"error al crear un trabajador", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def buscar_por_rut(request):
        Trabajador = apps.get_model('trabajador', 'Trabajador')
        rut = request.GET.get('rut', None)
        if not rut:
            return Response(
                {"error": "Debe proporcionar un RUT"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            trabajador = Trabajador.objects.get(rut=rut)
            serializer = TrabajadorSerializer(trabajador)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Trabajador.DoesNotExist:
            return Response(
                {"error": "Trabajador no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @staticmethod
    def buscar_por_nombre(request):
        Trabajador = apps.get_model('trabajador', 'Trabajador')
        nombre = request.GET.get('nombre', None)
        if not nombre:
            return Response(
                {"error": "Debe proporcionar un nombre"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        trabajadores = Trabajador.objects.filter(nombre__icontains=nombre)
        if not trabajadores.exists():
            return Response(
                {"error": "No se encontraron trabajadores con ese nombre"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TrabajadorSerializer(trabajadores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def buscar_por_correo(request):
        Trabajador = apps.get_model('trabajador', 'Trabajador')
        correo = request.GET.get('correo_electronico', None)
        if not correo:
            return Response(
                {"error": "Debe proporcionar un correo electrónico"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            trabajador = Trabajador.objects.get(correo_electronico=correo)
            serializer = TrabajadorSerializer(trabajador)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Trabajador.DoesNotExist:
            return Response(
                {"error": "Trabajador no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @staticmethod
    def listar_activos(request):
        Trabajador = apps.get_model('trabajador', 'Trabajador')
        trabajadores = Trabajador.objects.filter(estado=True)
        if not trabajadores.exists():
            return Response(
                {"error": "No hay trabajadores activos"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TrabajadorSerializer(trabajadores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def actualizar_trabajador(request):
        Trabajador = apps.get_model('trabajador', 'Trabajador')
        id_trabajador = request.data.get('id_trabajador', None)
        if not id_trabajador:
            return Response(
                {"error": "Debe proporcionar el ID del trabajador"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            trabajador = Trabajador.objects.get(id_trabajador=id_trabajador)
        except Trabajador.DoesNotExist:
            return Response(
                {"error": "Trabajador no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TrabajadorSerializer(trabajador, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "Error al actualizar los datos", "detalle": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def desactivar_trabajador(request):
        Trabajador = apps.get_model('trabajador', 'Trabajador')
        id_trabajador = request.data.get('id_trabajador', None)
        if not id_trabajador:
            return Response(
                {"error": "Debe proporcionar el ID del trabajador"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            trabajador = Trabajador.objects.get(id_trabajador=id_trabajador)
            trabajador.estado = False
            trabajador.save(update_fields=['estado'])
            serializer = TrabajadorSerializer(trabajador)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Trabajador.DoesNotExist:
            return Response(
                {"error": "Trabajador no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Error al desactivar el trabajador", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
"""
Query set para asignacion de roles
"""