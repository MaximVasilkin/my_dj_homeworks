from django.urls import path
from measurement.views import SensorCreateGetView, CurrentSensor


urlpatterns = [
                path('sensor/', SensorCreateGetView.as_view()),
                path('sensor/<pk>/', CurrentSensor.as_view())
               ]
