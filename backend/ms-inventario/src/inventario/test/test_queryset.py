# from django.test import SimpleTestCase

# class QuerysetInventarioTest(SimpleTestCase):
#     def test_temporalmente_omitido(self):
#         self.skipTest("Test aprobado")


from unittest import TestCase
from unittest.mock import patch, MagicMock
from rest_framework import status
from inventario.queryset import ProductosQuerySet


class ProductosQuerySetTest(TestCase):

    @patch('inventario.queryset.apps.get_model')
    @patch('inventario.queryset.ProductoSerializer')
    def test_listar_productos(self, mock_serializer_class, mock_get_model):
        mock_producto_model = MagicMock()
        mock_queryset = MagicMock()
        mock_producto_model.objects.all.return_value = mock_queryset
        mock_get_model.return_value = mock_producto_model

        mock_serializer = MagicMock()
        mock_serializer.data = [{'nombre': 'Ibuprofeno'}]
        mock_serializer_class.return_value = mock_serializer

        response = ProductosQuerySet.listar_productos()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'nombre': 'Ibuprofeno'}])

        print("Test 1 aprobado")

    @patch('inventario.queryset.apps.get_model')
    @patch('inventario.queryset.ProductoSerializer')
    def test_listar_producto_por_nombre(self, mock_serializer_class, mock_get_model):
        mock_request = MagicMock()
        mock_request.GET.get.return_value = 'ibuprofeno'

        mock_producto_model = MagicMock()
        mock_queryset = MagicMock()
        mock_producto_model.objects.filter.return_value = mock_queryset
        mock_get_model.return_value = mock_producto_model

        mock_serializer = MagicMock()
        mock_serializer.data = [{'nombre': 'Ibuprofeno'}]
        mock_serializer_class.return_value = mock_serializer

        response = ProductosQuerySet.listar_producto_por_nombre(mock_request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'nombre': 'Ibuprofeno'}])
        mock_producto_model.objects.filter.assert_called_once_with(nombre__icontains='ibuprofeno')

        print("Test 2 aprobado")

    def test_listar_producto_por_nombre_sin_parametro(self):
        mock_request = MagicMock()
        mock_request.GET.get.return_value = None

        response = ProductosQuerySet.listar_producto_por_nombre(mock_request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Debe proporcionar un nombre de producto'})

        print("Test 3 aprobado")

    @patch('inventario.queryset.apps.get_model')
    @patch('inventario.queryset.ProductoSerializer')
    def test_consultar_producto_por_id(self, mock_serializer_class, mock_get_model):
        mock_request = MagicMock()
        mock_request.GET.get.return_value = '123'

        mock_producto_model = MagicMock()
        mock_queryset = MagicMock()
        mock_producto_model.objects.filter.return_value = mock_queryset
        mock_get_model.return_value = mock_producto_model

        mock_serializer = MagicMock()
        mock_serializer.data = [{'id_producto': '123'}]
        mock_serializer_class.return_value = mock_serializer

        response = ProductosQuerySet.consultar_producto_por_id(mock_request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id_producto': '123'}])

        print("Test 4 aprobado")

    def test_consultar_producto_por_id_sin_parametro(self):
        mock_request = MagicMock()
        mock_request.GET.get.return_value = None

        response = ProductosQuerySet.consultar_producto_por_id(mock_request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Debe proporcionar un ID de producto'})

        print("Test 5 aprobado")

    @patch('inventario.queryset.ProductoSerializer')
    def test_crear_producto_exitoso(self, mock_serializer_class):
        mock_request = MagicMock()
        mock_request.data = {'nombre': 'Nuevo producto'}

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = {'nombre': 'Nuevo producto'}
        mock_serializer_class.return_value = mock_serializer

        response = ProductosQuerySet.crear_producto(mock_request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'nombre': 'Nuevo producto'})
        mock_serializer.save.assert_called_once()

        print("Test 6 aprobado")

    @patch('inventario.queryset.ProductoSerializer')
    def test_crear_producto_invalido(self, mock_serializer_class):
        mock_request = MagicMock()
        mock_request.data = {}

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {'nombre': ['Este campo es requerido']}
        mock_serializer_class.return_value = mock_serializer

        response = ProductosQuerySet.crear_producto(mock_request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'nombre': ['Este campo es requerido']})
        
        print("Test 7 aprobado")