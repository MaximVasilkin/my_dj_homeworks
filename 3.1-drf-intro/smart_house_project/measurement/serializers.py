from rest_framework import serializers

from .models import Measurement, Sensor


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(SensorSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta(SensorSerializer.Meta):
        fields = ['id', 'name', 'description', 'measurements']
