from celery import shared_task
import requests
import json
from .models import Request
from django.core.mail import send_mail

# ทำให้ทำงานแบบ asynchronous ได้

@shared_task
def notify_provider(request_id, topic, status, recipient_email, user_id):
    try:
        # # ส่งแจ้งเตือนไปยัง Provider (เช่น Webhook, Email)
        message2 = {"recipient_email": recipient_email, "user": user_id , "request_id": str(request_id) , "topic": topic, "status": status}
        response = requests.post("http://127.0.0.1:8002/notify/create-notification/", json=message2)

        print(f"Notification sent: {response.status_code}")

        subject = f"Notification: {topic}"
        message = f"Request {request_id} is now {status}."
    
        send_mail(subject, message, "no-reply@yourapp.com", [recipient_email])

        return f"Email sent to {recipient_email} for request {request_id}"
    
    except Request.DoesNotExist:
        return {"error": "Request not found"}
    
@shared_task
def create_tracking(request, start_date, end_date, iot_set_id):
    try:
        # # ส่งแจ้งเตือนไปยัง Provider (เช่น Webhook, Email)
        message2 = {"request": request, "start_date": start_date , "end_date": end_date , "iot_set_id": iot_set_id}
        response = requests.post("http://127.0.0.1:8004/tracking/create/", json=message2)

        print(f" Tracking created: {response.status_code}")
    
    except Request.DoesNotExist:
        return {"error": "Request not found"}

