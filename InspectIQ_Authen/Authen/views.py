from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from allauth.socialaccount.models import SocialToken

from django.views.generic import TemplateView

class ProfileView(TemplateView):
    template_name = 'profile.html'

class CheckLoginStatusView(APIView):
    """
    ตรวจสอบสถานะการล็อกอินของผู้ใช้
    """

    permission_classes = [IsAuthenticated]  # ต้องล็อกอินก่อนถึงจะเข้าถึง API นี้ได้

    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email
        })


class GetUserTokenView(APIView):
    """
    ดึง Token ของ User เพื่อให้ Project_A และ Project_B ใช้งาน
    """

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=401)

        try:
            token = SocialToken.objects.get(account__user=request.user, account__provider='google')
            return Response({"token": token.token})
        except SocialToken.DoesNotExist:
            return Response({"error": "Token not found"}, status=404)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileAPIView(APIView):

    def get(self, request, user_id=None):
        try:
            # ถ้าไม่มี user_id -> ดึงข้อมูลของตัวเอง
            if user_id is None:
                user = request.user
            else:
                user = User.objects.get(id=user_id)

            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            })
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)