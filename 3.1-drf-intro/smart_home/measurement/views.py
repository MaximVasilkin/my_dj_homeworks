from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer


class SensorCreateGetView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class CurrentSensor(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    def post(self, request, pk):
        data = request.data
        sensor = Sensor.objects.filter(id=pk)[0]
        temperature = data.get('temperature')
        measurement = Measurement(sensor_id=sensor, temperature=temperature)
        measurement.save()
        return Response({"added sensor's measurement": temperature})


