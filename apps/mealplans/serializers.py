"""
REST API Serializers for Meal Plans App
"""
from rest_framework import serializers
from django.db import models
from .models import MealPlan, Meal
from apps.recipes.serializers import RecipeListSerializer


class MealSerializer(serializers.ModelSerializer):
    """Serializer for Meal model"""
    recipe = RecipeListSerializer(read_only=True)
    recipe_id = serializers.IntegerField(write_only=True, source='recipe.id')
    meal_type_display = serializers.CharField(source='get_meal_type_display', read_only=True)
    day_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = Meal
        fields = [
            'id', 'meal_plan', 'recipe', 'recipe_id',
            'meal_type', 'meal_type_display', 'day_of_week', 'day_display',
            'date', 'servings', 'notes', 'is_completed', 'total_calories', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        recipe_id = validated_data.pop('recipe', {}).get('id')
        from apps.recipes.models import Recipe
        recipe = Recipe.objects.get(id=recipe_id)
        validated_data['recipe'] = recipe
        return super().create(validated_data)


class MealPlanListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for meal plan lists"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = MealPlan
        fields = [
            'id', 'user', 'user_username', 'name', 'description',
            'start_date', 'end_date', 'is_active', 'is_current',
            'total_recipes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class MealPlanDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual meal plan view"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    meals = MealSerializer(many=True, read_only=True)
    
    class Meta:
        model = MealPlan
        fields = [
            'id', 'user', 'user_username', 'name', 'description',
            'start_date', 'end_date', 'is_active', 'is_current',
            'total_recipes', 'meals', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class MealPlanCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating meal plans"""
    
    class Meta:
        model = MealPlan
        fields = ['name', 'description', 'start_date', 'end_date', 'is_active']
