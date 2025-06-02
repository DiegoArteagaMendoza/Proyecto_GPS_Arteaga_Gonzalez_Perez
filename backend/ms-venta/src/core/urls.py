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
from django.urls import path
from venta.views import listar_ventas, realizar_venta, listar_venta_ultimos_30_dias, listar_venta_por_rut
from venta.views import listar_boletas, realizar_boleta, listar_boleta_por_rut

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_prometheus.urls')),
    #venta
    path('listar/venta/', listar_ventas, name='listar-ventas'),
    path('realizar/venta/', realizar_venta, name='realizar-venta'),
    path('listar/venta/ultimos30dias/', listar_venta_ultimos_30_dias, name='listar-venta-ultimos-30-dias'),
    path('listar/venta/rut/', listar_venta_por_rut, name='listar-venta-por-rut'),
    #boleta
    path('listar/boleta/', listar_boletas, name='listar-boletas'),
    path('realizar/boleta/', realizar_boleta, name='realizar-boleta'),
    path('listar/boleta/rut/', listar_boleta_por_rut, name='listar-boleta-por-rut'),
]
