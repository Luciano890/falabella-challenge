from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'name',
            'lastname',
            'id_type',
            'id_number',
            'email',
            'phone',
            'address',
        ]
