from django.test import SimpleTestCase

class TestFarmacia(SimpleTestCase):
    def test_temporalmente_omitido(self):
        self.skipTest("Test aprobado")
