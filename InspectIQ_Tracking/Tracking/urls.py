from django.urls import path
# from .views import CheckAuthStatusView
from .views import CreateTrackingView, UpdateTrackingStatusView

urlpatterns = [
    path("create/", CreateTrackingView.as_view(), name="create_tracking"),
    path("update/", UpdateTrackingStatusView.as_view(), name="update_tracking"),
]
