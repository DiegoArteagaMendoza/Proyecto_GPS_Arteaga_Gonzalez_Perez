from rest_framework import serializers
from .models import Farmacia

class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = [
            'id_farmacia', 'nombre_farmacia', 'direccion', 'comuna'
        ]
        read_only_fields = ('id_farmacia',)