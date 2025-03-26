from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Notification
from django.contrib.auth.models import User

@method_decorator(csrf_exempt, name='dispatch')
class CreateLogNotifyView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            recipient_email = data.get("recipient_email")
            user_id = data.get("user")  
            request_id = data.get("request_id")
            topic = data.get("topic")
            status = data.get("status")
            
            
            
            new_notification = Notification.objects.create(
                recipient_email=recipient_email,
                user_id=user_id,  
                request_id=request_id,
                topic=topic,
                status=status
            )
            

            return JsonResponse({"message": "Request received", "request_id": str(new_notification.id)})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
