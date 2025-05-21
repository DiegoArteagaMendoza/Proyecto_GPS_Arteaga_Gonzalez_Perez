import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from src.inventario.models import Producto

@pytest.mark.django_db
def test_listar_productos_retorna_lista_correcta():
    Producto.objects.create(nombre="Producto 1", descripcion="Desc 1")
    Producto.objects.create(nombre="Producto 2", descripcion="Desc 2")

    client = APIClient()
    url = reverse('listar-todos-los-productos') 
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['nombre'] == "Producto 1"
