# from django.test import SimpleTestCase

# class QuerysetFarmaciaTest(SimpleTestCase):
#     def test_temporalmente_omitido(self):
#         self.skipTest("Test aprobado")


from unittest import TestCase
from unittest.mock import patch, MagicMock
from rest_framework import status
from farmacia.queryset import FarmaciasQuerySet


class FarmaciasQuerySetTest(TestCase):

    @patch('farmacia.queryset.apps.get_model')
    @patch('farmacia.queryset.FarmaciaSerializer')
    def test_listar_farmacias(self, mock_serializer_class, mock_get_model):
        # Simulamos que Farmacia.objects.all() retorna un mock
        mock_farmacia_model = MagicMock()
        mock_queryset = MagicMock()
        mock_farmacia_model.objects.all.return_value = mock_queryset
        mock_get_model.return_value = mock_farmacia_model

        # Simulamos el serializer
        mock_serializer = MagicMock()
        mock_serializer.data = [{'nombre': 'Farmacia A'}]
        mock_serializer_class.return_value = mock_serializer

        # Ejecutamos el método
        response = FarmaciasQuerySet.listar_farmacias()

        # Verificamos respuesta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'nombre': 'Farmacia A'}])

        # Verificamos que se llamaron correctamente
        mock_get_model.assert_called_with('farmacia', 'Farmacia')
        mock_farmacia_model.objects.all.assert_called_once()
        mock_serializer_class.assert_called_with(mock_queryset, many=True)

        print("Test listar farmacias ejecutado correctamente")

    @patch('farmacia.queryset.FarmaciaSerializer')
    def test_crear_farmacia_exitosa(self, mock_serializer_class):
        # Mocks del request
        mock_request = MagicMock()
        mock_request.data = {'nombre': 'Nueva Farmacia'}

        # Configuramos el serializer
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = {'nombre': 'Nueva Farmacia'}
        mock_serializer_class.return_value = mock_serializer

        # Ejecutamos
        response = FarmaciasQuerySet.crear_farmacia(mock_request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'nombre': 'Nueva Farmacia'})
        mock_serializer.save.assert_called_once()

        print("Test crear farmacia exitosa ejecutado correctamente")

    @patch('farmacia.queryset.FarmaciaSerializer')
    def test_crear_farmacia_invalida(self, mock_serializer_class):
        mock_request = MagicMock()
        mock_request.data = {}

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {'nombre': ['Este campo es requerido.']}
        mock_serializer_class.return_value = mock_serializer

        response = FarmaciasQuerySet.crear_farmacia(mock_request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'nombre': ['Este campo es requerido.']})

        print("Test crear farmacia invalida ejecutado correctamente")
