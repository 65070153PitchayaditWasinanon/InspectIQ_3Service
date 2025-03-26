from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from allauth.socialaccount.models import SocialToken
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework import generics
# from .models import User
# from .serializers import UserSerializer

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

#fam
# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()  # ดึงข้อมูลทั้งหมดจาก User
#     serializer_class = UserSerializer  # ใช้ serializer ในการแปลงข้อมูลเป็น JSON
#     lookup_field = 'id'  # กำหนดให้ค้นหาจาก id

# class UserList(APIView):
#     def get(self, request, user_id):
#         user = get_object_or_404(User, id=user_id)  # ถ้าไม่พบจะคืนค่า 404
#         serializer = UserSerializer(user)  # แปลงข้อมูลเป็น JSON
#         return Response(serializer.data, status=status.HTTP_200_OK)