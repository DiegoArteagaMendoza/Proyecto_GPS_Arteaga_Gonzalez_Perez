from django.apps import apps
from django.db import models
from django.db.models import F, Q
from regex import T
from rest_framework.response import Response
from rest_framework import status
from .serializers import FarmaciaSerializer, RolSerializer, TrabajadorSerializer, AsignacionRolSerializer

"""
Querys para Farmacia Serializer
"""
class FarmaicaQuerySet(models.QuerySet):
    @staticmethod
    def listar_farmacias():
        Farmacia = apps.get_model('trabajador', 'Farmacia')    
        respuesta = Farmacia.objects.all()
        serializer = FarmaciaSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def listar_farmacias_por_nombre(request):
        Farmacia = apps.get_model('trabajador', 'Farmacia')
        nombre = request.GET.get('nombre')
        if not nombre:
            return Response({'error': 'Debe proporcionar un nombre de farmacia'}, status=status.HTTP_400_BAD_REQUEST)
        respuesta = Farmacia.objects.filter(nombre=nombre)
        serializer = FarmaciaSerializer(respuesta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def crear_farmacia(request):
        serializer = FarmaciaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error":"error al crear una farmacia", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
class AsignacionRolQuerySet(models.QuerySet):
    @staticmethod
    def crear_asignacion(request):
        AsignacionRol = apps.get_model('trabajador', 'AsignacionRol')
        Trabajador = apps.get_model('trabajador', 'Trabajador')
        Rol = apps.get_model('trabajador', 'Rol')
        from .serializers import AsignacionRolSerializer  # Importa aquí para evitar ciclos

        # Validar campos requeridos
        id_trabajador = request.data.get('id_trabajador')
        id_rol = request.data.get('id_rol')

        if not id_trabajador or not id_rol:
            return Response(
                {"error": "Debe proporcionar id_trabajador e id_rol"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar que existan las relaciones
        try:
            Trabajador.objects.get(id_trabajador=id_trabajador)
            Rol.objects.get(id_rol=id_rol)
        except Trabajador.DoesNotExist:
            return Response(
                {"error": "Trabajador no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Rol.DoesNotExist:
            return Response(
                {"error": "Rol no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validar que no exista una asignación activa duplicada
        if AsignacionRol.objects.filter(
            id_trabajador=id_trabajador,
            id_rol=id_rol,
            activo=True
        ).exists():
            return Response(
                {"error": "El trabajador ya tiene esta asignación activa"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serializar y guardar
        serializer = AsignacionRolSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": "Error al crear la asignación", "detalle": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def listar_todas(request):
        AsignacionRol = apps.get_model('trabajador', 'AsignacionRol')
        from .serializers import AsignacionRolSerializer

        asignaciones = AsignacionRol.objects.all()
        if not asignaciones.exists():
            return Response(
                {"error": "No hay asignaciones registradas"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = AsignacionRolSerializer(asignaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def listar_activas(request):
        AsignacionRol = apps.get_model('trabajador', 'AsignacionRol')
        from .serializers import AsignacionRolSerializer

        asignaciones = AsignacionRol.objects.filter(activo=True)
        if not asignaciones.exists():
            return Response(
                {"error": "No hay asignaciones activas"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = AsignacionRolSerializer(asignaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def listar_inactivas(request):
        AsignacionRol = apps.get_model('trabajador', 'AsignacionRol')
        from .serializers import AsignacionRolSerializer

        asignaciones = AsignacionRol.objects.filter(activo=False)
        if not asignaciones.exists():
            return Response(
                {"error": "No hay asignaciones inactivas"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = AsignacionRolSerializer(asignaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def actualizar_asignacion(request):
        AsignacionRol = apps.get_model('trabajador', 'AsignacionRol')
        from .serializers import AsignacionRolSerializer

        id_asignacion = request.data.get('id_asignacion_rol')
        if not id_asignacion:
            return Response(
                {"error": "Debe proporcionar el ID de la asignación"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            asignacion = AsignacionRol.objects.get(id_asignacion_rol=id_asignacion)
        except AsignacionRol.DoesNotExist:
            return Response(
                {"error": "Asignación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AsignacionRolSerializer(asignacion, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "Error al actualizar la asignación", "detalle": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def desactivar_asignacion(request):
        AsignacionRol = apps.get_model('trabajador', 'AsignacionRol')
        from .serializers import AsignacionRolSerializer

        id_asignacion = request.data.get('id_asignacion_rol')
        if not id_asignacion:
            return Response(
                {"error": "Debe proporcionar el ID de la asignación"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            asignacion = AsignacionRol.objects.get(id_asignacion_rol=id_asignacion)
            asignacion.activo = False
            asignacion.save(update_fields=['activo'])
            serializer = AsignacionRolSerializer(asignacion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AsignacionRol.DoesNotExist:
            return Response(
                {"error": "Asignación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Error al desactivar la asignación", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    def reactivar_asignacion(request):
        AsignacionRol = apps.get_model('trabajador', 'AsignacionRol')
        from .serializers import AsignacionRolSerializer

        id_asignacion = request.data.get('id_asignacion_rol')
        if not id_asignacion:
            return Response(
                {"error": "Debe proporcionar el ID de la asignación"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            asignacion = AsignacionRol.objects.get(id_asignacion_rol=id_asignacion)
            if asignacion.activo:
                return Response(
                    {"error": "La asignación ya está activa"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            asignacion.activo = True
            asignacion.save(update_fields=['activo'])
            serializer = AsignacionRolSerializer(asignacion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AsignacionRol.DoesNotExist:
            return Response(
                {"error": "Asignación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Error al reactivar la asignación", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )