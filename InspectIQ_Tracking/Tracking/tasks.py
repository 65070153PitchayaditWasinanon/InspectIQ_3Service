from celery import shared_task
import requests
import json
from django.core.mail import send_mail

@shared_task
def notify_temp_and_humid_provider(request_id, topic, recipient_email):
    try:
        # # ส่งแจ้งเตือนไปยัง Provider (เช่น Webhook, Email)
        # message2 = {"recipient_email": recipient_email, "user": user_id , "request_id": str(request_id) , "topic": topic, "status": status}
        # response = requests.post("http://127.0.0.1:8002/notify/create-notification/", json=message2)

        # print(f"Notification sent: {response.status_code}")



        subject = f"Notification: {topic}"
        message = f"Request {request_id} is now ."
    
        send_mail(subject, message, "no-reply@yourapp.com", [recipient_email])

        return f"Email sent to {recipient_email} for request {request_id}"
    
    except Request.DoesNotExist:
        return {"error": "Request not found"}