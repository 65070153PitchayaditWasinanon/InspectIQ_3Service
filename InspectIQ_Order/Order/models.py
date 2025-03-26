import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # ใช้ User จาก Authen Service

class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.IntegerField(null=True)  # คนส่งคำขอ (Customer)
    topic = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    category = models.JSONField()
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ], default='pending')

    def __str__(self):
        return f"{self.topic} - {self.status}"

