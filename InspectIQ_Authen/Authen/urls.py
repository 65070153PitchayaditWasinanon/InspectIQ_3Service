from django.urls import path
from .views import CheckLoginStatusView, GetUserTokenView

urlpatterns = [
    path('check-login/', CheckLoginStatusView.as_view(), name='check_login'),
    path('get-token/', GetUserTokenView.as_view(), name='get_token'),
]
