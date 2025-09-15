from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer
from rest_framework import serializers


class SensorCreateView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SensorUpdateView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SensorDetailSerializer
        else:
            return SensorSerializer


class MeasurementCreateView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def perform_create(self, serializer):
        sensor_id = self.request.data.get('sensor')
        try:
            sensor = Sensor.objects.get(id = sensor_id)  # Проверяем существование датчика
        except Sensor.DoesNotExist:
            raise serializers.ValidationError("Датчик не найден")

        measure = serializer.save(sensor = sensor)


