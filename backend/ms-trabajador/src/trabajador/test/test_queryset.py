# from django.test import SimpleTestCase

# class QuerysetTestTrabajador(SimpleTestCase):
#     def test_temporalmente_omitido(self):
#         self.skipTest("Test aprobado")


from unittest import TestCase
from unittest.mock import patch, MagicMock
from rest_framework import status
from trabajador.queryset import RolesQuerySet, TrabajadorQuerySet


class RolesQuerySetTest(TestCase):

    @patch('trabajador.queryset.RolSerializer')
    def test_crear_rol_exitoso(self, mock_serializer_class):
        mock_request = MagicMock()
        mock_request.data = {'nombre_rol': 'Admin'}

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = {'nombre_rol': 'Admin'}
        mock_serializer_class.return_value = mock_serializer

        response = RolesQuerySet.crear_rol(mock_request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'nombre_rol': 'Admin'})
        print("✔ Test crear_rol_exitoso ejecutado correctamente")

    @patch('trabajador.queryset.RolSerializer')
    @patch('trabajador.queryset.apps.get_model')
    def test_listar_roles(self, mock_get_model, mock_serializer_class):
        mock_model = MagicMock()
        mock_queryset = MagicMock()
        mock_model.objects.all.return_value = mock_queryset
        mock_get_model.return_value = mock_model

        mock_serializer = MagicMock()
        mock_serializer.data = [{'nombre_rol': 'Admin'}]
        mock_serializer_class.return_value = mock_serializer

        response = RolesQuerySet.listar_roles()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'nombre_rol': 'Admin'}])
        print("✔ Test listar_roles ejecutado correctamente")

    @patch('trabajador.queryset.apps.get_model')
    def test_buscar_rol_existente(self, mock_get_model):
        mock_model = MagicMock()
        mock_model.objects.filter.return_value.exists.return_value = True
        mock_get_model.return_value = mock_model

        result = RolesQuerySet.buscar_rol('Admin')

        self.assertTrue(result)
        print("✔ Test buscar_rol_existente ejecutado correctamente")


class TrabajadorQuerySetTest(TestCase):

    @patch('trabajador.queryset.TrabajadorSerializer')
    @patch('trabajador.queryset.RolesQuerySet.buscar_rol')
    @patch('trabajador.queryset.apps.get_model')
    def test_crear_trabajador_exitoso(self, mock_get_model, mock_buscar_rol, mock_serializer_class):
        mock_request = MagicMock()
        mock_request.data = {
            'rol': 'Admin',
            'correo_electronico': 'test@email.com',
            'contrasena': '1234'
        }

        mock_buscar_rol.return_value = True
        mock_model = MagicMock()
        mock_model.objects.filter.return_value.first.return_value = None
        mock_get_model.return_value = mock_model

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = {'nombre': 'Juan'}
        mock_serializer_class.return_value = mock_serializer

        response = TrabajadorQuerySet.crear_trabajador(mock_request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'nombre': 'Juan'})
        print("✔ Test crear_trabajador_exitoso ejecutado correctamente")

    @patch('trabajador.queryset.TrabajadorSerializer')
    @patch('trabajador.queryset.apps.get_model')
    def test_buscar_por_rut_exitoso(self, mock_get_model, mock_serializer_class):
        mock_request = MagicMock()
        mock_request.GET.get.return_value = '12345678-9'

        mock_trabajador = MagicMock()
        mock_get_model.return_value.objects.get.return_value = mock_trabajador

        mock_serializer = MagicMock()
        mock_serializer.data = {'rut': '12345678-9'}
        mock_serializer_class.return_value = mock_serializer

        response = TrabajadorQuerySet.buscar_por_rut(mock_request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'rut': '12345678-9'})
        print("✔ Test buscar_por_rut_exitoso ejecutado correctamente")

    def test_buscar_por_rut_sin_parametro(self):
        mock_request = MagicMock()
        mock_request.GET.get.return_value = None

        response = TrabajadorQuerySet.buscar_por_rut(mock_request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Debe proporcionar un RUT'})
        print("✔ Test buscar_por_rut_sin_parametro ejecutado correctamente")
