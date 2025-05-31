from django.db import models
from django.core.validators import MinLengthValidator

# ----------------------------
# Tabla: usuarios
# ----------------------------
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True, validators=[MinLengthValidator(9)], verbose_name="RUT")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150, unique=True)
    contraseña = models.TextField(verbose_name="Contraseña")
    telefono = models.CharField(max_length=20, blank=True, null=True)
    rol = models.CharField(max_length=50, choices=[('cliente', 'Cliente'), ('admin', 'Admin'), ('farmaceutico', 'Farmacéutico')], default='cliente')
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"

    class Meta:
        db_table = 'usuarios'
        managed = False


# ----------------------------
# Tabla: farmacias
# ----------------------------
class Farmacia(models.Model):
    id_farmacia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(max_length=150, unique=True)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'farmacias'
        managed = False


# ----------------------------
# Tabla intermedia: usuarios_farmacia
# ----------------------------
class UsuarioFarmacia(models.Model):
    id_usuario_farmacia = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario', related_name='farmacias_asignadas')
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE, db_column='id_farmacia', related_name='usuarios_asignados')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} -> {self.farmacia}"

    class Meta:
        db_table = 'usuarios_farmacia'
        unique_together = ('usuario', 'farmacia')
        managed = False


# ----------------------------
# Tabla: productos
# ----------------------------
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'productos'
        managed = False


# ----------------------------
# Tabla: ProductosFarmacia
# ----------------------------
class ProductoFarmacia(models.Model):
    id_producto_farmacia = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE, db_column='id_producto', related_name='farmacias')
    id_farmacia = models.ForeignKey('Farmacia', on_delete=models.CASCADE, db_column='id_farmacia', related_name='productos')
    stock = models.IntegerField()
    disponible = models.BooleanField(default=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.producto.nombre} en {self.farmacia.nombre}"

    class Meta:
        db_table = 'productos_farmacia'
        # unique_together = ('producto', 'farmacia')
        managed = False


# ----------------------------
# Tabla: medicamentos_cliente
# ----------------------------
class MedicamentoCliente(models.Model):
    id_medicamento_cliente = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario_cliente', related_name='medicamentos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto', related_name='clientes')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    retiro = models.BooleanField(default=False)
    fecha_retiro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.producto}"

    class Meta:
        db_table = 'medicamentos_cliente'
        # unique_together = ('usuario', 'producto')
        managed = False
