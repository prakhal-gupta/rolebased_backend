from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from .base.api.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .routers import restricted_router
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

schema_view = get_schema_view(
    openapi.Info(
        title="ERP API",
        default_version='v1',
        description="LAWSPHERE APIs",
        contact=openapi.Contact(email="prakhalgupta.j12@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lawsphere-api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('lawsphere-api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('lawsphere-api/v1/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('lawsphere-api/v1/password_reset/', include('django_rest_passwordreset.urls')),
    path('lawsphere-api/v1/', include(restricted_router.urls)),
]

if settings.DEBUG:
    swagger_url = [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
    urlpatterns = urlpatterns + swagger_url
