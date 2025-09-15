from rest_framework import serializers
from .models import Sensor, Measurement

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']

class MeasurementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at' ]

class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementDetailSerializer(many = True, read_only = True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
