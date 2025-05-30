from django.db import models
from django.core.validators import MinValueValidator

# Modelo rol
class Rol (models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=255, null=False, unique=True)
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre_rol
    
    class Meta:
        db_table = "rol"
        managed=False

# Modelo: Trabajador
class Trabajador(models.Model):
    id_trabajador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False, verbose_name="Nombre")
    apellido = models.CharField(max_length=255, null=False, verbose_name="Apellido")
    rut = models.CharField(max_length=20, null=False, unique=True, verbose_name="RUT")
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    correo_electronico = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Correo Electrónico")
    fecha_contratacion = models.DateField(auto_now_add=True, verbose_name="Fecha de Contratación")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    rol = models.CharField(max_length=100, null=False)
    contrasena = models.CharField(max_length=255, null=True, verbose_name="Contrasena")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = 'trabajador'
        managed = False
