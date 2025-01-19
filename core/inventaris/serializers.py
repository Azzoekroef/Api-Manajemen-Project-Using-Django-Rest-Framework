from rest_framework import serializers
from .models import Inventaris_status,Inventaris

class InventarisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventaris
        fields = "__all__"