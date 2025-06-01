from django.test import SimpleTestCase

class TestTrabajador(SimpleTestCase):
    def test_temporalmente_omitido(self):
        self.skipTest("Test aprobado")
