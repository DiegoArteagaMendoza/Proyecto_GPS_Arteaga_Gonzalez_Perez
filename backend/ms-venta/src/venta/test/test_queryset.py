# from django.test import SimpleTestCase

# class QuerysetVentaTest(SimpleTestCase):
#     def test_temporalmente_omitido(self):
#         self.skipTest("Test aprobado")


from unittest import TestCase
from unittest.mock import patch, MagicMock
from rest_framework import status
from venta.queryset import VentaQuerySet
from datetime import timedelta
from django.utils import timezone


class VentaQuerySetTest(TestCase):

    # @patch('venta.queryset.apps.get_model')
    # @patch('venta.queryset.VentaSerializer')
    # def test_listar_ventas(self, mock_serializer_class, mock_get_model):
    #     mock_venta_model = MagicMock()
    #     mock_queryset = MagicMock()
    #     mock_venta_model.objects.all.return_value = mock_queryset
    #     mock_get_model.return_value = mock_venta_model

    #     mock_serializer = MagicMock()
    #     mock_serializer.data = [{'id_venta': 1}]
    #     mock_serializer_class.return_value = mock_serializer

    #     response = VentaQuerySet.listar_ventas()

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, [{'id_venta': 1}])
    #     mock_get_model.assert_called_with('venta', 'Venta')
    #     mock_venta_model.objects.all.assert_called_once()
    #     mock_serializer_class.assert_called_with(mock_queryset, many=True)

    #     print("Test listar_ventas ejecutado correctamente")

    @patch('venta.queryset.apps.get_model')
    @patch('venta.queryset.VentaSerializer')
    def test_listar_venta_ultimos_30_dias(self, mock_serializer_class, mock_get_model):
        mock_venta_model = MagicMock()
        mock_queryset = MagicMock()
        mock_venta_model.objects.filter.return_value = mock_queryset
        mock_get_model.return_value = mock_venta_model

        mock_serializer = MagicMock()
        mock_serializer.data = [{'id_venta': 2}]
        mock_serializer_class.return_value = mock_serializer

        response = VentaQuerySet.listar_venta_ultimos_30_dias()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id_venta': 2}])
        mock_venta_model.objects.filter.assert_called_once()
        mock_serializer_class.assert_called_with(mock_queryset, many=True)

        print("Test listar_venta_ultimos_30_dias ejecutado correctamente")

    @patch('venta.queryset.apps.get_model')
    @patch('venta.queryset.VentaSerializer')
    def test_listar_venta_por_rut(self, mock_serializer_class, mock_get_model):
        mock_request = MagicMock()
        mock_request.GET.get.return_value = '12345678-9'

        mock_venta_model = MagicMock()
        mock_queryset = MagicMock()
        mock_venta_model.objects.filter.return_value = mock_queryset
        mock_get_model.return_value = mock_venta_model

        mock_serializer = MagicMock()
        mock_serializer.data = [{'rut_cliente': '12345678-9'}]
        mock_serializer_class.return_value = mock_serializer

        response = VentaQuerySet.listar_venta_por_rut(mock_request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'rut_cliente': '12345678-9'}])
        mock_get_model.assert_called_with('venta', 'Venta')
        mock_venta_model.objects.filter.assert_called_once()
        mock_serializer_class.assert_called_with(mock_queryset, many=True)

        print("Test listar_venta_por_rut ejecutado correctamente")

    @patch('venta.queryset.apps.get_model')
    def test_listar_ventas_por_rut_con_detalle(self, mock_get_model):
        mock_request = MagicMock()
        mock_request.GET.get.return_value = '12345678-9'

        mock_venta_model = MagicMock()
        mock_venta_instance = MagicMock()
        mock_venta_instance.id_venta = 1
        mock_venta_instance.fecha_venta.strftime.return_value = '2024-01-01 12:00'
        mock_venta_instance.rut_cliente = '12345678-9'
        mock_venta_instance.total_venta = 20000
        mock_venta_instance.metodo_pago = 'efectivo'
        mock_venta_instance.estado_venta = 'completado'
        mock_venta_instance.farmacia = 'Farmacia Central'

        mock_detalle = MagicMock()
        mock_detalle.id_producto = 10
        mock_detalle.nombre_producto = 'Paracetamol'
        mock_detalle.cantidad = 2
        mock_detalle.precio_unitario = 1000
        mock_detalle.subtotal = 2000

        mock_venta_instance.detalles.all.return_value = [mock_detalle]
        mock_venta_model.objects.filter.return_value = [mock_venta_instance]
        mock_get_model.return_value = mock_venta_model

        response = VentaQuerySet.listar_ventas_por_rut_con_detalle(mock_request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id_venta': 1,
            'fecha_venta': '2024-01-01 12:00',
            'rut_cliente': '12345678-9',
            'total_venta': 20000.0,
            'metodo_pago': 'efectivo',
            'estado_venta': 'completado',
            'farmacia': 'Farmacia Central',
            'productos': [{
                'id_producto': 10,
                'nombre_producto': 'Paracetamol',
                'cantidad': 2.0,
                'precio_unitario': 1000.0,
                'subtotal': 2000.0
            }]
        }])

        print("Test listar_ventas_por_rut_con_detalle ejecutado correctamente")
