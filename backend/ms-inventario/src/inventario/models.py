from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'productos'
        managed = False

class Bodega(models.Model):
    id_bodega = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    ubicacion = models.TextField(blank=True, null=True, verbose_name="Ubicación")
    farmacia = models.CharField(max_length=255, verbose_name="Farmacia")
    estado = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"

    class Meta:
        db_table = 'bodegas'
        managed = False

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventarios', verbose_name="Producto", db_column='id_producto')
    nombre_producto = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre del Producto")
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='inventarios', verbose_name="Bodega", db_column='id_bodega')
    lote = models.CharField(max_length=100, blank=True, null=True, verbose_name="Lote")
    fecha_lote = models.DateField(blank=True, null=True, verbose_name="Fecha del Lote")
    fecha_vencimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Vencimiento")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)], verbose_name="Cantidad")
    unidad_medida = models.CharField(max_length=50, blank=True, null=True, verbose_name="Unidad de Medida")
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000, verbose_name="Costo Unitario")
    costo_promedio = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000, verbose_name="Costo Promedio")
    precio_venta = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000, verbose_name="Precio de Venta")
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock Mínimo")

    def __str__(self):
        return f"{self.producto.nombre} en {self.bodega.nombre} - Lote: {self.lote}"

    class Meta:
        db_table = 'inventario'
        managed = False
        indexes = [
            models.Index(fields=['producto']),
            models.Index(fields=['bodega']),
        ]

class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    id_movimiento = models.AutoField(primary_key=True)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='movimientos', verbose_name="Inventario", db_column='id_inventario')
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES, verbose_name="Tipo de Movimiento")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Cantidad")
    fecha_movimiento = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Movimiento")
    observacion = models.TextField(blank=True, null=True, verbose_name="Observación")
    usuario = models.CharField(max_length=100, blank=True, null=True, verbose_name="Usuario")

    def __str__(self):
        return f"{self.tipo_movimiento.capitalize()} - {self.cantidad} | {self.inventario.producto.nombre}"

    class Meta:
        db_table = 'movimientos_inventario'
        managed = False
        indexes = [
            models.Index(fields=['fecha_movimiento']),
        ]