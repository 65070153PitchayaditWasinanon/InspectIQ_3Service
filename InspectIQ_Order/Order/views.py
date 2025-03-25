from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Request
from .tasks import process_request, process_order, notify_provider

@method_decorator(csrf_exempt, name='dispatch')
class CreateRequestView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            topic = data.get("topic")
            description = data.get("description")
            category = data.get("category", [])
            recipient_email = "fraction042@gmail.com"

            new_request = Request.objects.create(
                user_id=user_id,
                topic=topic,
                description=description,
                category=category
            )

            task = notify_provider.delay(new_request.id, topic, new_request.status, recipient_email)
            # ส่งไปให้ Celery ทำงาน
            # task = process_request.delay(str(new_request.id))

            return JsonResponse({"message": "Request received", "task_id": task.id, "request_id": str(new_request.id)})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "Method not allowed"}, status=405) # or return a help message.
    
@method_decorator(csrf_exempt, name='dispatch')
class AcceptRequestView(View):
    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            request_id = data.get("request_id")

            req = Request.objects.get(id=request_id)

            status = data.get("status")

            req.status = status
            
            req.save()

            if status == "approved":

                # task = notify_provider.delay(request_id)
                return JsonResponse({"message": "Request accepted successfully","task_id": "task.id", "request_id": str(request_id)})
            else:
                return JsonResponse({"status": "Request is rejected"})

            # {"status": "Request is approved"}
            # return JsonResponse()

        except Request.DoesNotExist:
            return JsonResponse({"error": "Request not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
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

# OAuth2 Google Account

import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

class CheckAuthStatusView(APIView):
    """
    เรียก API จาก `Authen` เพื่อตรวจสอบว่าผู้ใช้ Login แล้วหรือยัง
    """

    def get(self, request):
        token = request.headers.get("Authorization")  # ดึง Token จาก Header
        if not token:
            return Response({"error": "Missing Token"}, status=401)

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(settings.AUTH_SERVER_URL, headers=headers)  # เช็คสถานะการล็อกอิน

        if response.status_code == 200:
            return Response(response.json())  # ส่งข้อมูล User กลับไป
        return Response({"error": "Unauthorized"}, status=401)



@method_decorator(csrf_exempt, name='dispatch')
class NotifyProviderView(View):
    def post(self, request, *args, **kwargs):
        try:
            # รับข้อมูล JSON ที่ส่งมาใน body
            data = json.loads(request.body)
            request_id = data.get("request_id")
            # topic = data.get("topic")
            # status = data.get("status")

            # อัปเดตหรือสร้าง Notification ใหม่
            # notification, created = Notification.objects.update_or_create(
            #     request_id=request_id,
            #     defaults={"topic": topic, "status": status}
            # )

            # ส่ง Response กลับ
            return JsonResponse({
                "message": "Notification saved",
                "request_id": request_id
            }, status=200)
           
            # "created": created  # True ถ้าเป็นการสร้างใหม่, False ถ้าเป็นการอัปเดต
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
