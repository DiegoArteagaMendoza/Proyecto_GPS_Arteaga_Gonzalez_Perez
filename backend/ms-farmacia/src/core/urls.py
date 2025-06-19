from django.urls import path, include
from django.contrib import admin
from farmacia.views import listar_farmacias, crear_farmacia

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_prometheus.urls')),
    path("farmacias/", listar_farmacias, name="listar-farmacias"),
    path("farmacias/registar/", crear_farmacia, name="registrar-farmacia"),
    path("ruta/prueba/farmacia/", listar_farmacias, name="listar-farmacias"),
]
