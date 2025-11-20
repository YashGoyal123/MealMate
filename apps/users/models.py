"""
Custom User Model for MealMate
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
import string


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    """
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    
    # Dietary Preferences
    dietary_preferences = models.ManyToManyField(
        'recipes.DietaryTag',
        related_name='users',
        blank=True
    )
    
    # User metrics
    favorite_recipes = models.ManyToManyField(
        'recipes.Recipe',
        related_name='favorited_by',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
    
    @property
    def recipe_count(self):
        """Return the number of recipes created by this user"""
        return self.recipes.count()
    
    @property
    def meal_plan_count(self):
        """Return the number of meal plans created by this user"""
        return self.meal_plans.count()


class EmailVerificationOTP(models.Model):
    """
    Model to store OTP for email verification
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes', null=True, blank=True)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email Verification OTP'
        verbose_name_plural = 'Email Verification OTPs'
    
    def __str__(self):
        return f"OTP for {self.email} - {self.otp}"
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # OTP expires in 10 minutes
            self.expires_at = timezone.now() + timedelta(minutes=10)
        if not self.otp:
            # Generate 6-digit OTP
            self.otp = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)
    
    def is_expired(self):
        """Check if OTP has expired"""
        return timezone.now() > self.expires_at
    
    def verify(self, otp_input):
        """Verify the OTP"""
        if self.is_expired():
            return False, "OTP has expired"
        if self.is_verified:
            return False, "OTP has already been used"
        if self.otp == otp_input:
            self.is_verified = True
            self.save()
            return True, "Email verified successfully"
        return False, "Invalid OTP"
