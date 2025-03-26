from rest_framework import serializers
from .models import Tracking

class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = ['id', 'request', 'iot_set_id']  # หรือคุณอาจจะใส่ฟิลด์ทั้งหมดที่ต้องการอัพเดท
