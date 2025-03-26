from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Tracking
# from .tasks import process_request, process_order, notify_provider
from django.contrib.auth.models import User
import requests




@method_decorator(csrf_exempt, name='dispatch')
class CreateTrackingView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            request = data.get("request")
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            iot_set_id = data.get("iot_set_id", [])

            # recipient_email = "fraction042@gmail.com"
            new_Tracking = Tracking.objects.create(
                request=request,
                start_date=start_date,
                end_date=end_date,
                iot_set_id=iot_set_id,
            )
            # ส่งไปให้ Celery ทำงาน
            # task = process_request.delay(str(new_request.id))

            return JsonResponse({"message": "Tracking ถูกสร้างเรียบร้อย", "task_id":" task.id", "request_id": str(new_Tracking.id)})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# @method_decorator(csrf_exempt, name='dispatch')
# class UpdateTrackingStatusView(View):
#     def put(self, request, *args, **kwargs):
#         try:
#             data = json.loads(request.body)
#             request = data.get("request")
#             iot_set_id = data.get("iot_set_id")
#             req = Tracking.objects.get(request=request)

#             # recipient_email = "fraction042@gmail.com"
#             req.iot_set_id = iot_set_id
#             req.save()
#             # if 30 <= req.iot_set_id['temperature'] <= 25:
#             #     print("High")
#             # else:
#             #     print("Low")
#             # ส่งไปให้ Celery ทำงาน
#             # task = process_request.delay(str(new_request.id))

#             return JsonResponse({"message": "Tracking ถูกสร้างเรียบร้อย", "task_id":" task.id", "request_id": "str(new_Tracking.id)"})

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tracking
from .serializers import TrackingSerializer
import json
import urllib.parse
from .tasks import notify_temp_and_humid_provider


class UpdateTrackingStatusView(APIView):
    def get(self, request, *args, **kwargs):
        # ดึงข้อมูลจาก query parameters
        iot_set_id = request.query_params.get('iot_set_id', None)  # ดึงค่า iot_set_id

        # ตรวจสอบว่ามีการส่ง iot_set_id มาหรือไม่
        if iot_set_id:
            # ทำการ decode URL และแปลงเป็น JSON
            try:
                # Decode ข้อมูลที่เข้ารหัสแล้ว
                decoded_data = urllib.parse.unquote(iot_set_id)
                iot_set_data = json.loads(decoded_data)  # แปลงสตริง JSON เป็นข้อมูล Python dict
                tracking_instance = Tracking.objects.get(iot_set_id__contains={"id": iot_set_data["id"]})
                return Response({"request_id": tracking_instance.request}, status=status.HTTP_200_OK)
            except (json.JSONDecodeError, TypeError):
                return Response({"error": "Invalid iot_set_id format"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "iot_set_id not provided"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            # รับข้อมูล JSON จาก request
            data = request.data
            request_param = data.get("request")
            iot_set_id = data.get("iot_set_id")
            provider_email = "fraction042@gmail.com"

            if iot_set_id["temperature"] >= 30 or iot_set_id["temperature"] <= 20:
                #แจ้งเตือน
                topic = "อุณหภูมิผิดปกติ"
                task = notify_temp_and_humid_provider.delay(request_param, topic, provider_email)
            else:
                pass
            if iot_set_id["humidity"] >= 50 or iot_set_id["humidity"] <= 30:
                #แจ้งเตือน
                topic = "ความชื้นผิดปกติ"
                task = notify_temp_and_humid_provider.delay(request_param, topic, provider_email)
            else:
                pass
            # หาข้อมูล Tracking ตาม request
            tracking_instance = Tracking.objects.get(request=request_param)

            # สร้าง serializer สำหรับอัพเดทข้อมูล
            serializer = TrackingSerializer(tracking_instance, data=data)
            if serializer.is_valid():
                # อัพเดทข้อมูล
                serializer.save()
                return Response({
                    "message": "Tracking ถูกอัพเดทเรียบร้อย",
                    "task_id": "task.id",  # คุณอาจจะใส่ task_id ของ Celery ถ้ามี
                    "request_id": str(tracking_instance.id)
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Tracking.DoesNotExist:
            return Response({"error": "Tracking not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
