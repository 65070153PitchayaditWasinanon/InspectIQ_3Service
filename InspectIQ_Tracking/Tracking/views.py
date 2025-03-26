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
                iot_set_id=iot_set_id
            )    
            # ส่งไปให้ Celery ทำงาน
            # task = process_request.delay(str(new_request.id))

            return JsonResponse({"message": "Tracking ถูกสร้างเรียบร้อย", "task_id":" task.id", "request_id": str(new_Tracking.id)})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)