from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Venta")
    rut_cliente = models.CharField(max_length=20, blank=False, null=False, verbose_name="RUT Cliente")
    total_venta = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Total Venta")
    metodo_pago = models.CharField(max_length=50, blank=False, null=False, verbose_name="Método de Pago")
    estado_venta = models.CharField(max_length=20, default='completada', verbose_name="Estado de Venta")
    farmacia = models.CharField(max_length=255, verbose_name="Farmacia")

    def __str__(self):
        return f"Venta #{self.id_venta} - {self.fecha_venta.strftime('%Y-%m-%d')}"

    class Meta:
        db_table = 'ventas'
        managed = False
        indexes = [
            models.Index(fields=['fecha_venta']),
        ]


class DetalleVenta(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles', db_column='id_venta', verbose_name="Venta")
    id_producto = models.IntegerField(blank=False, null=False, verbose_name="ID Producto")  # No FK porque es microservicio distinto
    nombre_producto = models.CharField(max_length=255, verbose_name="Nombre del Producto")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Precio Unitario")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Subtotal")

    def __str__(self):
        return f"{self.nombre_producto} x {self.cantidad}"

    class Meta:
        db_table = 'detalle_venta'
        managed = False


class Boleta(models.Model):
    id_boleta = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='boletas', db_column='id_venta', verbose_name="Venta")
    numero_boleta = models.CharField(max_length=100, verbose_name="Número Boleta")
    tipo_documento = models.CharField(max_length=50, default='boleta', verbose_name="Tipo de Documento")
    fecha_emision = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Emisión")
    total = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Total")
    rut_cliente = models.CharField(max_length=20, blank=True, null=True, verbose_name="RUT Cliente")
    nombre_cliente = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre Cliente")

    def __str__(self):
        return f"{self.tipo_documento.capitalize()} #{self.numero_boleta}"

    class Meta:
        db_table = 'boletas'
        managed = False
   