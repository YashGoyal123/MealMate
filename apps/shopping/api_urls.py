"""
API URL Configuration for Shopping App
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'shopping-lists', api_views.ShoppingListViewSet, basename='shoppinglist')
router.register(r'items', api_views.ShoppingListItemViewSet, basename='shoppinglistitem')

urlpatterns = [
    path('', include(router.urls)),
]
