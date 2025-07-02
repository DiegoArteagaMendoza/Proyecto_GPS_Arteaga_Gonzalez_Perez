from django.urls import path, include
from django.contrib import admin
from usuariocliente.views import listar_usuarios, crear_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('metrics/', include('django_prometheus.urls')),

    # urls para usuarios
    path('usuarios/', listar_usuarios, name="listar-todos-usuarios"),
    path('usuarios/registrar/', crear_usuario, name="registrar-usuario"),

]
