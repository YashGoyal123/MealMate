"""
Admin Configuration for Users App
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailVerificationOTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_picture', 'dietary_preferences', 'favorite_recipes'),
        }),
    )
    
    filter_horizontal = ['dietary_preferences', 'favorite_recipes']


@admin.register(EmailVerificationOTP)
class EmailVerificationOTPAdmin(admin.ModelAdmin):
    """Admin configuration for Email Verification OTP"""
    list_display = ['user', 'email', 'otp', 'created_at', 'expires_at', 'is_verified', 'is_expired_status']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'email', 'otp']
    readonly_fields = ['created_at', 'expires_at', 'otp']
    ordering = ['-created_at']
    
    def is_expired_status(self, obj):
        """Display if OTP is expired"""
        return obj.is_expired()
    is_expired_status.boolean = True
    is_expired_status.short_description = 'Expired'
