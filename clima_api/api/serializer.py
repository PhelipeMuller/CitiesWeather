
from rest_framework import serializers
from .models import CityWether

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CityWether
        fields = "__all__"
