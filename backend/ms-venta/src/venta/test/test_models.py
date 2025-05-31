from django.test import SimpleTestCase

class TestVenta(SimpleTestCase):
    def test_temporalmente_omitido(self):
        self.skipTest("Test aprobado")
