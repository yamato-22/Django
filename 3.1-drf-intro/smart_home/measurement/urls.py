from django.contrib import admin
from django.urls import path

from measurement.views import SensorCreateView, SensorUpdateView, MeasurementCreateView

urlpatterns = [
    path('sensors/', SensorCreateView.as_view(), name = 'sensor_create_view'),
    path('sensors/<int:pk>/', SensorUpdateView.as_view(), name = 'sensor_update_view'),
    path('measurements/', MeasurementCreateView.as_view(), name = 'measure_create'),
]
