"""
URL configuration for auction_bot project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Auction Bot API",
      default_version='v1',
      description="Smart Automated Bidding System with Phase-Based Bot Strategy",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@auctionbot.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Frontend routes for users (login, register pages)
    path('auth/', include('users.urls')),
    # Frontend routes for auctions at root level
    path('', include('auctions.urls')),
    # API routes
    path('api/auth/', include('users.api_urls')),  # API auth endpoints
    path('api/auctions/', include('auctions.api_urls')),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

