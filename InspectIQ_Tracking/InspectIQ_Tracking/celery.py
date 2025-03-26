import os
from celery import Celery

# ตั้งค่าตัวแปรสภาพแวดล้อมให้ Django ใช้ settings ของโปรเจกต์ InspectIQ_Order
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InspectIQ_Tracking.settings")

# ตั้งชื่อ Celery ให้ตรงกับชื่อโปรเจกต์
app = Celery("InspectIQ_Tracking")

# โหลดค่า config จาก settings.py ที่ขึ้นต้นด้วย "CELERY_"
app.config_from_object("django.conf:settings", namespace="CELERY")

# ให้ Celery ค้นหา tasks.py ในทุก App อัตโนมัติ
app.autodiscover_tasks()