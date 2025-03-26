from django.urls import path
# from .views import CheckAuthStatusView
from .views import CreateRequestView, AcceptRequestView
from django.urls import path
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# สร้าง schema view สำหรับ Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Tracking API",
        default_version='v1',
        description="API สำหรับการติดตามอุปกรณ์ IoT",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@trackingapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("request/", CreateRequestView.as_view(), name="create_request"),
    path("accept/", AcceptRequestView.as_view(), name="accept_request"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
