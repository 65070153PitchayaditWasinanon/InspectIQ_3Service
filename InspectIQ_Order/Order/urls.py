from django.urls import path
from .views import CreateRequestView, CreateOrderView, CheckAuthStatusView

urlpatterns = [
    path("create/", CreateRequestView.as_view(), name="create_request"),
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
]
