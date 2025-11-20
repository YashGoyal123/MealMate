"""
REST API Views for Meal Plans App
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import MealPlan, Meal
from .serializers import (
    MealPlanListSerializer, MealPlanDetailSerializer,
    MealPlanCreateUpdateSerializer, MealSerializer
)


class MealPlanViewSet(viewsets.ModelViewSet):
    """API endpoint for meal plans"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user).prefetch_related('meals__recipe')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MealPlanListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MealPlanCreateUpdateSerializer
        return MealPlanDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealViewSet(viewsets.ModelViewSet):
    """API endpoint for meals"""
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Meal.objects.filter(meal_plan__user=self.request.user).select_related('recipe', 'meal_plan')
