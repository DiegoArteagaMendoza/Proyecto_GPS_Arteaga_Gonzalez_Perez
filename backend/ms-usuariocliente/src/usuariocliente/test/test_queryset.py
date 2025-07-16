# from django.test import SimpleTestCase

# class QuerysetUsuarioTrabajadorTest(SimpleTestCase):
#     def test_temporalmente_omitido(self):
#         self.skipTest("Test aprobado")

from unittest import TestCase
from unittest.mock import patch, MagicMock
from rest_framework import status
from django.apps import apps
from usuariocliente.queryset import UsuarioQuerySet
from rest_framework.response import Response


class UsuarioQuerySetTest(TestCase):

    @patch('usuariocliente.queryset.UsuarioSerializer')
    @patch('usuariocliente.queryset.apps.get_model')
    def test_listar_usuarios_exitoso(self, mock_get_model, mock_serializer_class):
        # Configurar mocks
        mock_usuario_model = MagicMock()
        mock_queryset = MagicMock()
        mock_usuario_model.objects.all.return_value = mock_queryset
        mock_get_model.return_value = mock_usuario_model
        
        mock_serializer = MagicMock()
        mock_serializer.data = [{'nombre': 'Test User'}]
        mock_serializer_class.return_value = mock_serializer

        # Ejecutar método
        response = UsuarioQuerySet.listar_usuarios()

        # Verificar resultados
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'nombre': 'Test User'}])
        mock_usuario_model.objects.all.assert_called_once()
        mock_serializer_class.assert_called_once_with(mock_queryset, many=True)
        print("✔ Test listar_usuarios_exitoso ejecutado correctamente")

    @patch('usuariocliente.queryset.UsuarioSerializer')
    def test_crear_usuario_exitoso(self, mock_serializer_class):
        # Configurar mocks
        mock_request = MagicMock()
        mock_request.data = {'nombre': 'Test User', 'correo': 'test@example.com'}
        
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = {'nombre': 'Test User', 'correo': 'test@example.com'}
        mock_serializer_class.return_value = mock_serializer

        # Ejecutar método
        response = UsuarioQuerySet.crear_usuario(mock_request)

        # Verificar resultados
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'nombre': 'Test User', 'correo': 'test@example.com'})
        mock_serializer_class.assert_called_once_with(data=mock_request.data)
        mock_serializer.save.assert_called_once()
        print("✔ Test crear_usuario_exitoso ejecutado correctamente")

    @patch('usuariocliente.queryset.UsuarioSerializer')
    def test_crear_usuario_invalido(self, mock_serializer_class):
        # Configurar mocks
        mock_request = MagicMock()
        mock_request.data = {'nombre': '', 'correo': 'invalid'}
        
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {'correo': 'Invalid email'}
        mock_serializer_class.return_value = mock_serializer

        # Ejecutar método
        response = UsuarioQuerySet.crear_usuario(mock_request)

        # Verificar resultados
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'correo': 'Invalid email'})
        print("✔ Test crear_usuario_invalido ejecutado correctamente")

    @patch('usuariocliente.queryset.UsuarioSerializer')
    def test_crear_usuario_error_servidor(self, mock_serializer_class):
        # Configurar mocks
        mock_request = MagicMock()
        mock_request.data = {'nombre': 'Test', 'correo': 'test@example.com'}
        
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.save.side_effect = Exception("Database error")
        mock_serializer_class.return_value = mock_serializer

        # Ejecutar método
        response = UsuarioQuerySet.crear_usuario(mock_request)

        # Verificar resultados
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {
            "error": "Error al crear usuario", 
            "details": "Database error"
        })
        print("✔ Test crear_usuario_error_servidor ejecutado correctamente")

    @patch('usuariocliente.queryset.apps.get_model')
    def test_usuarios_retiro_24_horas(self, mock_get_model):
        # Configurar mocks
        mock_usuario_model = MagicMock()
        mock_queryset = MagicMock()
        
        expected_result = [{
            'nombre': 'Test',
            'apellido': 'User',
            'correo': 'test@example.com',
            'fecha_registro': '2023-01-01',
            'medicamentos': [],
            'retiro_en_dias': 1
        }]
        
        mock_usuario_model.objects.filter.return_value.values.return_value = expected_result
        mock_get_model.return_value = mock_usuario_model

        # Ejecutar método
        result = UsuarioQuerySet.usuarios_retiro_24_horas()

        # Verificar resultados
        self.assertEqual(result, expected_result)
        mock_usuario_model.objects.filter.assert_called_once_with(beneficiario=True)
        print("✔ Test usuarios_retiro_24_horas ejecutado correctamente")