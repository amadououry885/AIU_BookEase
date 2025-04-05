from rest_framework import serializers
from .models import Facility

class FacilitySerializer(serializers.ModelSerializer):  # Use ModelSerializer
    class Meta:
        model = Facility
        fields = ['id', 'name', 'description', 'price', 'availability', 'category']
