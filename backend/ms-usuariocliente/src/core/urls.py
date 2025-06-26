from django.urls import path, include
from django.contrib import admin
from usuariocliente.views import listar_usuarios, crear_usuario
from usuariocliente.views import listar_farmacias, crear_farmacia
from usuariocliente.views import listar_productos, consulta_nombre_producto, farmacias_con_producto_disponible

urlpatterns = [
    path('admin/', admin.site.urls),
    path('metrics/', include('django_prometheus.urls')),
    # urls para productos
    path('productos/', listar_productos, name="listar-todos-los-productos"),
    path('productos/consulta_nombre/', consulta_nombre_producto, name="consulta-nombre-producto"),
    path('productos/farmacias_con_producto_disponible/', farmacias_con_producto_disponible, name="farmacias-con-producto-disponible"),
    # urls para usuarios
    path('usuarios/', listar_usuarios, name="listar-todos-usuarios"),
    path('usuarios/registrar/', crear_usuario, name="registrar-usuario"),

    # urls para farmacias
    path('farmacias/', listar_farmacias, name="listar-todas-las-farmacias"),
    path('farmacias/registrar/', crear_farmacia, name="registrar-farmacia"),
]
