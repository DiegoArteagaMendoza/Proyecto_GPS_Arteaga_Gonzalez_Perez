from django.urls import path
from farmacia.views import listar_farmacias, crear_farmacia

urlpatterns = [
    path("farmacias/", listar_farmacias, name="listar-farmacias"),
    path("farmacias/registar/", crear_farmacia, name="registrar-farmacia"),
]
