from django.db import models
from django.utils.timezone import now


class Notification(models.Model):
    recipient_email = models.EmailField()# ผู้รับ
    user_id = models.IntegerField(null=True)
    request_id = models.CharField(max_length=255)  # อ้างอิง Request
    topic = models.CharField(max_length=255)  # หัวข้อ
    status = models.CharField(max_length=100)  # สถานะ (เช่น "Shipped", "Completed")
    sent_at = models.DateTimeField(default=now)  # เวลาที่แจ้งเตือน
    is_sent = models.BooleanField(default=False)  # เช็คว่าส่งแล้วหรือยัง

    def __str__(self):
        return f"{self.topic} - {self.status} ({self.recipient_email})" 
