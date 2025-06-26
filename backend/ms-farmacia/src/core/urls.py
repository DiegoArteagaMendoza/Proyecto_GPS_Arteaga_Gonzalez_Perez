from django.urls import path, include
from django.contrib import admin
from farmacia.views import listar_farmacias, crear_farmacia, metrics_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('metrics/', metrics_view, name="metricas"),
    path("farmacias/", listar_farmacias, name="listar-farmacias"),
    path("farmacias/registrar/", crear_farmacia, name="registrar-farmacia"),
    # path("RutaPrueba/", crear_farmacia, name="Ruta-de-prueba")
]
