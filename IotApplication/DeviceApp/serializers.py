from rest_framework import serializers
from .models import Device,TemperatureReadings,HumidityReadings

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device
        fields="__all__"
class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model=TemperatureReadings
        fields="__all__"
class HumiditySerializer(serializers.ModelSerializer):
    class Meta:
        model=HumidityReadings
        fields="__all__"
        