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
    contrasena = models.TextField(verbose_name="Contraseña")
    telefono = models.CharField(max_length=20, blank=True, null=True)
    rol = models.CharField(max_length=50, choices=[('cliente', 'Cliente'), ('admin', 'Admin'), ('farmaceutico', 'Farmacéutico')], default='cliente')
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)

    # Nuevos atributos
    beneficiario = models.BooleanField(default=False)
    medicamentos = models.TextField(blank=True, null=True)
    retiro_en_dias = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"

    class Meta:
        db_table = 'usuarios_real'
        managed = False