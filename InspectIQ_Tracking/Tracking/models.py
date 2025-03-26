from django.db import models
import uuid

class Tracking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    iot_set_id = models.JSONField()  # เก็บ ID ของ IoT Devices ที่ใช้
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tracking for Request {self.request.id}"

# Received: {
# {
# 'id': '6acd5388-5fe6-4157-a943-b8c45543e02b',
# 'temperature': 23.11, 'humidity': 35.91,
# 'timestamp': '2025-03-26 21:03:24',
# 'name': 'IoT_Device_01'
# },
# {
# 'id': '6acd5388-5fe6-4157-a943-b8c45543e02b',
# 'temperature': 23.11, 'humidity': 35.91,
# 'timestamp': '2025-03-26 21:03:24',
# 'name': 'IoT_Device_01'
# },
#}