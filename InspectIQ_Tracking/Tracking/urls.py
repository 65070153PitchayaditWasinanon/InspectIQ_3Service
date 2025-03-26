from django.urls import path
# from .views import CheckAuthStatusView
from .views import CreateTrackingView

urlpatterns = [
    path("create/", CreateTrackingView.as_view(), name="create_tracking"),
]
