from rest_framework import serializers
from .models import Prueba

#valida los datos de la bdd
class PruebaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Prueba
        fields= [
            'id',
            'titulo',
            'telefono',
            'estado'
        ]
        read_only_fields=('id',)
