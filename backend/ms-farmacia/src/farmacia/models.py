from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class Farmacia(models.Model):
    id_farmacia = models.AutoField(primary_key=True)
    nombre_farmacia = models.CharField(max_length=255, verbose_name="Nombre")
    direccion = models.CharField(max_length=255, verbose_name="Direccion")
    comuna = models.CharField(max_length=255, verbose_name="Comuna")

    def __str__(self):
        return self.nombre_farmacia
    
    class Meta:
        db_table = 'farmacia'
        managed = True