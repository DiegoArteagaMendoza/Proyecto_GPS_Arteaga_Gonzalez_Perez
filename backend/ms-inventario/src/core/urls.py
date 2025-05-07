from django.urls import path
from inventario.views import obtener_inventario_completo, buscar_inventario_por_nombre_producto, buscar_inventario_por_lote, buscar_inventario_por_bodega, buscar_inventario_por_id_producto, obtener_inventario_bajo_stock, registrar_inventario
from inventario.views import listar_productos, listar_producto_por_nombre, consultar_producto_por_id, crear_producto
from inventario.views import obtener_bodegas, obtener_bodega_por_id, obtener_bodega_por_nombre, obtener_bodega_por_ubicacion, obtener_bodega_por_estado, registrar_bodega

urlpatterns = [
    # urls para productos
    path('productos/', listar_productos, name="listar-todos-los-productos"),
    path('productos/buscar/nombre/', listar_producto_por_nombre, name="listar-producto-por-nombre"),
    path('productos/buscar/id/', consultar_producto_por_id, name="listar-productos-por-id"),
    path('productos/registrar/', crear_producto, name="registrar-producto"),

    # urls para bodegas
    path('bodegas/', obtener_bodegas, name="listar-todas-las-bodegas"),
    path('bodegas/buscar/id/', obtener_bodega_por_id, name="listar-bodega-por-id"),
    path('bodegas/buscar/nombre/', obtener_bodega_por_nombre, name="listar-bodega-por-nombre"),
    path('bodegas/buscar/ubicacion/', obtener_bodega_por_ubicacion, name="listar-bodega-por-ubicacion"),
    path('bodegas/buscar/estado/', obtener_bodega_por_estado, name="listar-bodega-por-estado"),
    path('bodegas/', obtener_bodegas, name="listar-todas-las-bodegas"),
    path('bodegas/registrar/', registrar_bodega, name="registrar-bodega"),

    # urls para inventario
    path('inventario/', obtener_inventario_completo, name='inventario-completo'),
    path('inventario/buscar/nombre/', buscar_inventario_por_nombre_producto, name='buscar-por-nombre'),
    path('inventario/buscar/id-producto/', buscar_inventario_por_id_producto, name='buscar-por-id-producto'),
    path('inventario/buscar/lotes/', buscar_inventario_por_lote, name='buscar-por-lote'),
    path('inventario/bajo-stock/', obtener_inventario_bajo_stock, name='inventario-bajo-stock'),
    path('inventario/buscar/bodega/', buscar_inventario_por_bodega, name='buscar-por-bodega'),
    path('inventario/registrar/', registrar_inventario, name='registrar-inventario'),
]
