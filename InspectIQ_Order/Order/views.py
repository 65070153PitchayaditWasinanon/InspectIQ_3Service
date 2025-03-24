from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Request
from .tasks import process_request, process_order

@method_decorator(csrf_exempt, name='dispatch')
class CreateRequestView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            topic = data.get("topic")
            description = data.get("description")
            category = data.get("category", [])

            new_request = Request.objects.create(
                user_id=user_id,
                topic=topic,
                description=description,
                category=category
            )

            # ส่งไปให้ Celery ทำงาน
            task = process_request.delay(str(new_request.id))

            return JsonResponse({"message": "Request received", "task_id": task.id, "request_id": str(new_request.id)})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "Method not allowed"}, status=405) # or return a help message.

@method_decorator(csrf_exempt, name='dispatch')
class CreateOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            # รับข้อมูลจาก JSON ใน request body
            data = json.loads(request.body)
            order_id = data.get('order_id')  # รับ order_id

            if order_id:
                # ส่ง order_id ไปให้ Celery ทำงาน
                process_order.delay(order_id)
                return JsonResponse({"status": "Order is being processed"})
            else:
                return JsonResponse({"status": "Order ID is missing"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
