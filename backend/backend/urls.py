"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse

# Настройка Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="Food Delivery API",
        default_version='v1',
        description="API для сервиса доставки еды",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def healthcheck(request):
    return HttpResponse("ok")

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Prometheus metrics
    path('', include('django_prometheus.urls')),
    
    # Swagger UI URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Остальные URL-пути вашего приложения
    path("api/", include([
        path("auth/", include("djoser.urls")),
        path("auth/", include("djoser.urls.jwt")),
        path("auth/", include("djoser.urls.authtoken")),
        path("users/", include("users.urls")),
        path("", include("products.urls")),
        path("", include("basket.urls")),
        path("", include("orders.urls")),
    ])),
    path('healthcheck/', healthcheck),  # Новый эндпоинт для healthcheck
]

# Маршруты для статических файлов и медиа
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)