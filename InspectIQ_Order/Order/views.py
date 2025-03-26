from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Request
from .tasks import notify_provider, create_tracking
from django.contrib.auth.models import User
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

AUTHEN_SERVICE_URL = "http://127.0.0.1:8001/api/api/user/"



@method_decorator(csrf_exempt, name='dispatch')
class CreateRequestView(APIView):

    @swagger_auto_schema(
        operation_description="Create a new request",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID (required)'),
                'topic': openapi.Schema(type=openapi.TYPE_STRING, description='Topic of the request (required)'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the request (required)'),
                'category': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='List of categories (optional)'),
            },
            required=['user_id', 'topic', 'description'],  # กำหนดว่าอะไรที่ต้องมี
        ),
        responses={
            201: openapi.Response('Request created successfully', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'task_id': openapi.Schema(type=openapi.TYPE_STRING),
                'request_id': openapi.Schema(type=openapi.TYPE_STRING),
            })),
            400: 'Invalid data',
        }
    )

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

            task = notify_provider.delay(new_request.id, topic, new_request.status, recipient_email, user_id)

            return JsonResponse({"message": "Request received", "task_id": task.id, "request_id": str(new_request.id)})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)



    
@method_decorator(csrf_exempt, name='dispatch')
class AcceptRequestView(APIView):

    @swagger_auto_schema(
        operation_description="Accept or reject a request",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'request_id': openapi.Schema(type=openapi.TYPE_STRING, description='Request ID (required)'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the request (required)'),
                'start_date': openapi.Schema(type=openapi.TYPE_STRING, description='Start date in YYYY-MM-DD format (required)'),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING, description='End date in YYYY-MM-DD format (required)'),
                'iot_set_id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description='List of IoT set IDs (required)'),
            },
            required=['request_id', 'status', 'start_date', 'end_date', 'iot_set_id'],  # กำหนดว่าอะไรที่ต้องมี
        ),
        responses={
            200: openapi.Response('Request accepted successfully', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'task_id': openapi.Schema(type=openapi.TYPE_STRING),
                'request_id': openapi.Schema(type=openapi.TYPE_STRING),
            })),
            400: 'Invalid data',
            404: 'Request not found',
        }
    )

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            request_id = data.get("request_id")
            status = data.get("status")
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            iot_set_id = data.get("iot_set_id")

            req = Request.objects.get(id=request_id)

            req.status = status
            
            req.save()

            user_response = requests.get(f"{AUTHEN_SERVICE_URL}{req.user_id}/") 

            if user_response.status_code != 200:
                return JsonResponse({"error": "User not found in Authen Service"}, status=404)
            
            user_data = user_response.json()
            user_email = user_data.get("email")  
            
            if status == "approved":
                
                task = notify_provider.delay(request_id, req.topic, req.status, user_email, req.user_id)
                task2 = create_tracking.delay(request_id, start_date, end_date, iot_set_id)
                return JsonResponse({"message": "Request accepted successfully","task1_id": task.id ,"task2_id": task2.id, "request_id": str(request_id)})
            else:
                return JsonResponse({"status": "Request is rejected"})


        except Request.DoesNotExist:
            return JsonResponse({"error": "Request not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        

