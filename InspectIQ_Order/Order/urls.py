from django.urls import path
# from .views import CheckAuthStatusView
from .views import CreateRequestView, CreateOrderView, AcceptRequestView, NotifyProviderView

urlpatterns = [
    path("create/", CreateRequestView.as_view(), name="create_request"),
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path("accept/", AcceptRequestView.as_view(), name="accept_request"),
    path('notify/', NotifyProviderView.as_view(), name='notify_provider'),
]
