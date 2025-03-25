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
