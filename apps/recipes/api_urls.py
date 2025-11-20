"""
API URL Configuration for Recipes App
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'dietary-tags', api_views.DietaryTagViewSet)
router.register(r'recipes', api_views.RecipeViewSet, basename='recipe')
router.register(r'reviews', api_views.ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
