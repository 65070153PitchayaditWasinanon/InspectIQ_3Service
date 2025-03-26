from django.urls import path
from .views import LatestIoTDeviceAPIView

urlpatterns = [
    path('latest-iot-device/', LatestIoTDeviceAPIView.as_view(), name='latest-iot-device'),
]
