from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps.users import views as user_views

# API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="MealMate API",
        default_version='v1',
        description="Recipe Management and Meal Planning API",
        terms_of_service="https://www.mealmate.com/terms/",
        contact=openapi.Contact(email="contact@mealmate.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Home
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Custom signup with OTP verification (override allauth signup)
    path('accounts/signup/', user_views.custom_signup, name='account_signup'),
    
    # Authentication (allauth)
    path('accounts/', include('allauth.urls')),
    
    # Apps
    path('recipes/', include('apps.recipes.urls')),
    path('meal-plans/', include('apps.mealplans.urls')),
    path('shopping/', include('apps.shopping.urls')),
    path('users/', include('apps.users.urls')),
    
    # API
    path('api/recipes/', include('apps.recipes.api_urls')),
    path('api/meal-plans/', include('apps.mealplans.api_urls')),
    path('api/shopping/', include('apps.shopping.api_urls')),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom Admin Configuration
admin.site.site_header = "MealMate Administration"
admin.site.site_title = "MealMate Admin"
admin.site.index_title = "Welcome to MealMate Admin Panel"
