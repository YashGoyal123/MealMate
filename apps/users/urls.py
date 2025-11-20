"""
URL Configuration for users app
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # OTP verification (standalone)
    path('send-otp/', views.send_verification_otp, name='send_otp'),
    path('verify-otp/<int:otp_id>/', views.verify_otp, name='verify_otp'),
    path('resend-otp/<int:otp_id>/', views.resend_otp, name='resend_otp'),
    
    # Signup with OTP verification
    path('signup/', views.custom_signup, name='custom_signup'),
    path('verify-signup-otp/<int:otp_id>/', views.verify_signup_otp, name='verify_signup_otp'),
    path('resend-signup-otp/<int:otp_id>/', views.resend_signup_otp, name='resend_signup_otp'),
    
    # Account management
    path('profile/', views.profile_update, name='profile_update'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
