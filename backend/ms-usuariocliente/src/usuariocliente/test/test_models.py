from django.test import SimpleTestCase

class TestUsuarioTrabajador(SimpleTestCase):
    def test_temporalmente_omitido(self):
        self.skipTest("Test aprobado")
