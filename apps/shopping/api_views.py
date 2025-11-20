"""
REST API Views for Shopping App
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ShoppingList, ShoppingListItem
from .serializers import ShoppingListSerializer, ShoppingListCreateSerializer, ShoppingListItemSerializer


class ShoppingListViewSet(viewsets.ModelViewSet):
    """API endpoint for shopping lists"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user).prefetch_related('items')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ShoppingListCreateSerializer
        return ShoppingListSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShoppingListItemViewSet(viewsets.ModelViewSet):
    """API endpoint for shopping list items"""
    serializer_class = ShoppingListItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ShoppingListItem.objects.filter(shopping_list__user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_purchased(self, request, pk=None):
        """Toggle item purchased status"""
        item = self.get_object()
        item.is_purchased = not item.is_purchased
        item.save()
        serializer = self.get_serializer(item)
        return Response(serializer.data)
