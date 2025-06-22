"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from trabajador.views import crear_rol, listar_roles
from trabajador.views import listar_trabajadores, buscar_trabajador_rut, buscar_trabajador_nombre, buscar_por_correo, actualizar_trabajador, desactivar_trabajador, crear_trabajador
from trabajador.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('metrics/', include('django_prometheus.urls')),
    # urls para roles
    path('roles/', listar_roles, name="listar-roles-disponibles"),
    path('roles/crear/', crear_rol, name="crear-nuevo-rol"),

    # urls para trabajadores
    path('trabajador/', listar_trabajadores, name="listar-trabajadores-activos"),
    path('trabajador/buscar/rut/', buscar_trabajador_rut, name="buscar-trabajador-por-rut"),
    path('trabajador/buscar/nombre/', buscar_trabajador_nombre, name="buscar-trabajador-por-nombre"),
    path('trabajador/buscar/correo/', buscar_por_correo, name="buscar-trabajador-por-correo"),
    path('trabajador/actualizar/', actualizar_trabajador, name="actualiar-datos-trabajador"),
    path('trabajador/desactivar/', desactivar_trabajador, name="desactivar-trabajador"),
    path('trabajador/registrar/', crear_trabajador, name="registrar-nuevo-trabajador"),

    # urls para login
    path('login/', login, name="login"),
    path('RutaDePrueba/', login, name="logout"),

]
