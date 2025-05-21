from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
# Modelo Farmacia
class Farmacia(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False, verbose_name="Nombre")

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'farmacia'
        managed = False

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
    id_departamento = models.ForeignKey(Farmacia, on_delete=models.CASCADE, db_column='id_departamento', verbose_name="Departamento")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = 'trabajador'
        managed = False


# Modelo intermedio: Asignación de Roles
class AsignacionRol(models.Model):
    id_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, db_column='id_trabajador')
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='id_rol')
    fecha_inicio = models.DateField(auto_now_add=True, verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(null=True, blank=True, verbose_name="Fecha de Fin")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'asignacion_rol'
        managed = False