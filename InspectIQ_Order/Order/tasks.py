from celery import shared_task
import requests
import json
from .models import Request
from django.core.mail import send_mail

# ทำให้ทำงานแบบ asynchronous ได้
@shared_task
def process_request(request_id):
    print(f"Processing request {request_id}")

    try:
        request = Request.objects.get(id=request_id)
        request.status = 'pending'  # อนุมัติอัตโนมัติ
        request.save()

        # แจ้งไปยัง Tracking Service
        message = json.dumps({"request_id": str(request_id)})
        response = requests.post("http://tracking-service:8002/new_request/", data=message)
        print(f"Sent to Tracking Service: {response.status_code}")

    except Request.DoesNotExist:
        print("Request not found")

    return {"status": "approved", "request_id": request_id}

@shared_task
def process_order(order_id):
    print(f"Processing order {order_id}")
    # คุณสามารถใส่ logic การประมวลผลจริงที่นี่ได้
    return {"status": "approved", "order_id": order_id}

@shared_task
def notify_provider(request_id, topic, status, recipient_email):
    try:
        # req = Request.objects.get(id=request_id)

        # # ส่งแจ้งเตือนไปยัง Provider (เช่น Webhook, Email)
        # message = {"request_id": str(req.id), "topic": req.topic, "status": req.status}
        # response = requests.post("http://127.0.0.1:8001/orders/notify/", json=message)

        # print(f"Notification sent: {response.status_code}")
        # # 
        # return {"status": "notified", "request_id": request_id}
        # 
        subject = f"Notification: {topic}"
        message = f"Request {request_id} is now {status}."
    
        send_mail(subject, message, "no-reply@yourapp.com", [recipient_email])

        return f"Email sent to {recipient_email} for request {request_id}"
    
    except Request.DoesNotExist:
        return {"error": "Request not found"}
    # print(f"Processing order {request_id}")
    # # คุณสามารถใส่ logic การประมวลผลจริงที่นี่ได้
    # return {"status": "approved22asdfsadf", "order_id": request_id}
