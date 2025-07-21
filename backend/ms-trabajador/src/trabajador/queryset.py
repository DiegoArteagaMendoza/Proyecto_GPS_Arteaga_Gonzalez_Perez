from django.apps import apps
from django.db import models
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import RolSerializer, TrabajadorSerializer
from django.contrib.auth.hashers import make_password, check_password
import requests
from rest_framework import status
from django.conf import settings
   
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
    
    @staticmethod
    def buscar_rol(rol):
        Rol = apps.get_model('trabajador', 'Rol')
        return Rol.objects.filter(nombre_rol=rol).exists()

            
"""
Query para trabajadores
"""
class TrabajadorQuerySet(models.QuerySet):

    @staticmethod
    def crear_trabajador(request):
        Trabajador = apps.get_model('trabajador', 'Trabajador')
        rol_nombre = request.data.get("rol")
        correo = request.data.get("correo_electronico")

        if not rol_nombre:
            return Response(
                {"error": "El parámetro 'rol' es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not correo:
            return Response(
                {"error": "El parámetro 'correo' es obligatorio"},
                status=status.HTTP_400_BAD_REQUEST
            )

        rol_obj = RolesQuerySet.buscar_rol(rol_nombre)
        if not rol_obj:
            return Response(
                {"error": f"El rol '{rol_nombre}' no existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        correo_obj = Trabajador.objects.filter(correo_electronico=correo).first()
        if correo_obj is not None:
            return Response(
                {"error": f"El correo '{correo}' ya se encuentra registrado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        if 'contrasena' in data:
            data['contrasena'] = make_password(data['contrasena'])

        serializer = TrabajadorSerializer(data=data)
        if serializer.is_valid():
            try:
                trabajador = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": "Error al crear el trabajador", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

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
        
class IniciarSesionQuerySet(models.QuerySet):
    @staticmethod
    def login(request):
        Trabajador = apps.get_model('trabajador', 'Trabajador')
        rut = request.data.get("rut", None)
        contrasena = request.data.get("contrasena", None)

        if not rut or not contrasena:
            return Response(
                {"error": "Debe proporcionar RUT y contraseña"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            trabajador = Trabajador.objects.get(rut=rut)
        except Trabajador.DoesNotExist:
            return Response(
                {"error": "Trabajador no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not trabajador.estado:
            return Response(
                {"error": "El trabajador está desactivado"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Verificar contraseña con check_password
        if check_password(contrasena, trabajador.contrasena):
            serializer = TrabajadorSerializer(trabajador)
            return Response("Login exitoso", status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Contraseña incorrecta"},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    # @staticmethod
    # def crear_usuario_cliente(request):
    #     """
    #     Envía datos al microservicio ms-usuariocliente para registrar un nuevo usuario.
    #     Si es beneficiario, procesa los medicamentos separados por ";"
    #     """
    #     try:
    #         url = "https://ms-usuariocliente-production.up.railway.app/usuarios/registrar/"
    #         data = request.data.copy()
            
    #         # Validar campos obligatorios
    #         campos_obligatorios = ['rut', 'nombre', 'apellido', 'correo', 'contraseña', 'rol']
    #         for campo in campos_obligatorios:
    #             if not data.get(campo):
    #                 return Response(
    #                     {"error": f"El campo '{campo}' es obligatorio"},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )
            
    #         # Si es beneficiario, procesar medicamentos
    #         if data.get('beneficiario', False):
    #             medicamentos_str = data.get('medicamentos', '')
                
    #             if medicamentos_str:
    #                 # Separar medicamentos por ";" y limpiar espacios
    #                 medicamentos_lista = [med.strip() for med in medicamentos_str.split(';') if med.strip()]
                    
    #                 # Validar que no esté vacío después del procesamiento
    #                 if not medicamentos_lista:
    #                     return Response(
    #                         {"error": "Debe proporcionar al menos un medicamento para beneficiarios"},
    #                         status=status.HTTP_400_BAD_REQUEST
    #                     )
                    
    #                 # Guardar tanto la lista como el string original
    #                 data['medicamentos_lista'] = medicamentos_lista
    #                 data['medicamentos_string'] = medicamentos_str
    #             else:
    #                 return Response(
    #                     {"error": "Los beneficiarios deben tener medicamentos asignados"},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )
            
    #         # Enviar al microservicio
    #         response = requests.post(url, json=data, timeout=30)
            
    #         # Procesar respuesta para el frontend
    #         if response.status_code == 201:
    #             response_data = response.json()
                
    #             # Si es beneficiario, agregar medicamentos procesados a la respuesta
    #             if data.get('beneficiario', False):
    #                 response_data['medicamentos_lista'] = data.get('medicamentos_lista', [])
    #                 response_data['total_medicamentos'] = len(data.get('medicamentos_lista', []))
                
    #             return Response(response_data, status=response.status_code)
    #         else:
    #             return Response(response.json(), status=response.status_code)

    #     except requests.exceptions.Timeout:
    #         return Response(
    #             {"error": "Timeout al conectar con el microservicio de usuario"}, 
    #             status=status.HTTP_504_GATEWAY_TIMEOUT
    #         )
    #     except requests.exceptions.RequestException as e:
    #         return Response(
    #             {"error": "Error al conectar con el microservicio de usuario", "detalle": str(e)}, 
    #             status=status.HTTP_503_SERVICE_UNAVAILABLE
    #         )
    #     except Exception as e:
    #         return Response(
    #             {"error": "Error interno del servidor", "detalle": str(e)}, 
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )

    @staticmethod
    def crear_usuario_cliente(request):
        """
        Envía datos al microservicio ms-usuariocliente para registrar un nuevo usuario.
        Si es beneficiario, procesa los medicamentos separados por ";"
        """
        try:
            url = "https://ms-usuariocliente-production.up.railway.app/usuarios/registrar/"
            data = request.data.copy()
            
            # Validar campos obligatorios
            # campos_obligatorios = ['rut', 'nombre', 'apellido', 'correo', 'contraseña', 'rol']
            # for campo in campos_obligatorios:
            #     if not data.get(campo):
            #         return Response(
            #             {"error": f"El campo '{campo}' es obligatorio"},
            #             status=status.HTTP_400_BAD_REQUEST
            #         )
            
            # Si es beneficiario, procesar medicamentos
            if data.get('beneficiario', False):
                medicamentos_str = data.get('medicamentos', '')
                
                if medicamentos_str:
                    medicamentos_lista = [med.strip() for med in medicamentos_str.split(';') if med.strip()]
                    
                    if not medicamentos_lista:
                        return Response(
                            {"error": "Debe proporcionar al menos un medicamento para beneficiarios"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    data['medicamentos_lista'] = medicamentos_lista
                    data['medicamentos_string'] = medicamentos_str
                else:
                    return Response(
                        {"error": "Los beneficiarios deben tener medicamentos asignados"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Depuración: imprimir el payload que se enviará
            print("Payload a enviar:", data)
            
            # Enviar al microservicio con headers explícitos
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            # Depuración: imprimir la respuesta cruda
            print("Respuesta cruda del microservicio:", response.text)
            
            # Procesar respuesta para el frontend
            try:
                response_json = response.json() if response.text else {}
            except ValueError as e:
                return Response(
                    {"error": "Respuesta inválida del microservicio", "detalle": str(e), "respuesta_cruda": response.text},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            
            if response.status_code == 201:
                # Si es beneficiario, agregar medicamentos procesados a la respuesta
                if data.get('beneficiario', False):
                    response_json['medicamentos_lista'] = data.get('medicamentos_lista', [])
                    response_json['total_medicamentos'] = len(data.get('medicamentos_lista', []))
                
                return Response(response_json, status=response.status_code)
            else:
                return Response(response_json, status=response.status_code)

        except requests.exceptions.Timeout:
            return Response(
                {"error": "Timeout al conectar con el microservicio de usuario"}, 
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": "Error al conectar con el microservicio de usuario", "detalle": str(e)}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {"error": "Error interno del servidor", "detalle": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )