from celery import shared_task
import requests
import json
from .models import Request

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
