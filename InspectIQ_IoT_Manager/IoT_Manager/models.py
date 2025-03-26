import uuid
from django.db import models

class IoTDevice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.timestamp}"