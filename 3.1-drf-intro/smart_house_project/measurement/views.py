from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorCreateGetView(APIView):
    def get(self, request):
        sensors = Sensor.objects.all()
        data = SensorSerializer(sensors, many=True).data
        return Response(data)

    def post(self, request):
        data = request.data
        sensor = SensorDetailSerializer(data=data)
        if sensor.is_valid():
            sensor.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({'create sensor status': 'error'})


class CurrentSensor(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    def put(self, request, pk):
        data = request.data
        sensor = Sensor.objects.get(pk=pk)
        name = data.get('name')
        description = data.get('description')
        if name:
            sensor.name = name
        if description:
            sensor.description = description
        sensor.save()
        return Response({'update sensor status': 'ok'})

    def patch(self, request, pk):
        data = request.data
        sensor = Sensor.objects.filter(id=pk)[0]
        temperature = data.get('temperature')
        measurement = Measurement(sensor_id=sensor, temperature=temperature)
        measurement.save()
        return Response({"added sensor's measurement": temperature})



# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
