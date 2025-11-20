"""
Quick test script to verify email configuration
Run this with: python test_email.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mealmate.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 50)
print("EMAIL CONFIGURATION TEST")
print("=" * 50)
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"Use TLS: {settings.EMAIL_USE_TLS}")
print(f"Host User: {settings.EMAIL_HOST_USER}")
print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
print("=" * 50)

try:
    print("\nSending test email...")
    send_mail(
        'Test Email from MealMate',
        'This is a test email to verify email configuration is working.',
        settings.DEFAULT_FROM_EMAIL,
        [settings.EMAIL_HOST_USER],  # Send to yourself
        fail_silently=False,
    )
    print("✅ Email sent successfully!")
    print(f"Check your inbox: {settings.EMAIL_HOST_USER}")
except Exception as e:
    print(f"❌ Error sending email: {e}")
    print("\nPossible issues:")
    print("1. Check your app password is correct (no spaces)")
    print("2. Make sure 2FA is enabled on your Google account")
    print("3. Check if 'Less secure app access' needs to be enabled")
    print("4. Verify your email address is correct")
