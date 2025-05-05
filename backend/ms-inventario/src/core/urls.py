from django.urls import path
from inventario.views import obtener_inventario_completo, buscar_inventario_por_nombre_producto, buscar_inventario_por_lote, buscar_inventario_por_bodega, buscar_inventario_por_id_producto, obtener_inventario_bajo_stock, registrar_inventario
from inventario.views import listar_productos, buscar_producto_por_id, buscar_producto_por_nombre, crear_producto
urlpatterns = [

    # urls para productos
    path('producto/', listar_productos, name='listar-productos'),
    path('producto/buscar/nombre/', buscar_producto_por_nombre, name='buscar-producto-por-nombre'),
    path('producto/buscar/id/', buscar_producto_por_id, name='buscar-producto-por-id'),
    path('producto/crear/', crear_producto, name='crear-producto'),
    
    # urls para inventario
    path('inventario/', obtener_inventario_completo, name='inventario-completo'),
    path('inventario/buscar/nombre/', buscar_inventario_por_nombre_producto, name='buscar-por-nombre'),
    path('inventario/buscar/id-producto/', buscar_inventario_por_id_producto, name='buscar-por-id-producto'),
    path('inventario/buscar/lote/', buscar_inventario_por_lote, name='buscar-por-lote'),
    path('inventario/bajo-stock/', obtener_inventario_bajo_stock, name='inventario-bajo-stock'),
    path('inventario/buscar/bodega/', buscar_inventario_por_bodega, name='buscar-por-bodega'),
    path('inventario/registrar/', registrar_inventario, name='registrar-inventario'),
]
