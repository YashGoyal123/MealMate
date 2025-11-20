"""
API URL Configuration for Meal Plans App
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'meal-plans', api_views.MealPlanViewSet, basename='mealplan')
router.register(r'meals', api_views.MealViewSet, basename='meal')

urlpatterns = [
    path('', include(router.urls)),
]
