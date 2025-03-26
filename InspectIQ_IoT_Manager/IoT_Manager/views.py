from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from .models import IoTDevice

class IoTDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoTDevice
        fields = '__all__'

class LatestIoTDeviceAPIView(APIView):
    permission_classes = [AllowAny]  # อนุญาตให้เข้าถึงได้จากทุกคน

    def get(self, request, *args, **kwargs):
        latest_device = IoTDevice.objects.order_by('-id').first()  # ดึงตัวล่าสุดตาม id
        if latest_device:
            serializer = IoTDeviceSerializer(latest_device)
            return Response(serializer.data)
        return Response({"error": "No IoTDevice data found"}, status=404)
