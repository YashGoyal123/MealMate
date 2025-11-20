"""
REST API Serializers for Shopping App
"""
from rest_framework import serializers
from .models import ShoppingList, ShoppingListItem


class ShoppingListItemSerializer(serializers.ModelSerializer):
    """Serializer for ShoppingListItem model"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = ShoppingListItem
        fields = [
            'id', 'shopping_list', 'name', 'quantity', 'category', 'category_display',
            'is_purchased', 'is_priority', 'notes', 'order', 'created_at'
        ]
        read_only_fields = ['created_at']


class ShoppingListSerializer(serializers.ModelSerializer):
    """Serializer for ShoppingList model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    items = ShoppingListItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = ShoppingList
        fields = [
            'id', 'user', 'user_username', 'meal_plan', 'name', 'notes',
            'is_completed', 'total_items', 'completed_items', 'completion_percentage',
            'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class ShoppingListCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating shopping lists"""
    
    class Meta:
        model = ShoppingList
        fields = ['meal_plan', 'name', 'notes', 'is_completed']
