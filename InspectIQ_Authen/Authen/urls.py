from django.urls import path
from .views import CheckLoginStatusView, GetUserTokenView, UserProfileAPIView

urlpatterns = [
    path('check-login/', CheckLoginStatusView.as_view(), name='check_login'),
    path('get-token/', GetUserTokenView.as_view(), name='get_token'),
    path('api/user/', UserProfileAPIView.as_view(), name='user-profile'),
    path('api/user/<int:user_id>/', UserProfileAPIView.as_view(), name='user-profile-detail'),
]
