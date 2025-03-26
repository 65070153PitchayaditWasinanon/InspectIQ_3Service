from django.urls import path
from .views import CreateLogNotifyView

urlpatterns = [
    path("create-notification/", CreateLogNotifyView.as_view(), name="create-notification"),
]
