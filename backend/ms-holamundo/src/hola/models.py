from django.db import models
class Prueba(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=50)
    objects = models.Manager()
    class Meta:
        db_table = 'prueba'
        managed = False

# Create your models here.
