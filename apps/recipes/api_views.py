"""
REST API Views for Recipes App
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, DietaryTag, Recipe, Review
from .serializers import (
    CategorySerializer, DietaryTagSerializer,
    RecipeListSerializer, RecipeDetailSerializer, RecipeCreateUpdateSerializer,
    ReviewSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class DietaryTagViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for dietary tags"""
    queryset = DietaryTag.objects.all()
    serializer_class = DietaryTagSerializer
    lookup_field = 'slug'


class RecipeViewSet(viewsets.ModelViewSet):
    """API endpoint for recipes"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'dietary_tags', 'difficulty']
    search_fields = ['title', 'description', 'ingredients__name']
    ordering_fields = ['created_at', 'title', 'prep_time', 'calories']
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = Recipe.objects.select_related('author', 'category').prefetch_related('dietary_tags')
        
        if self.request.user.is_authenticated:
            # Show public recipes and user's own recipes
            from django.db.models import Q
            queryset = queryset.filter(Q(is_public=True) | Q(author=self.request.user))
        else:
            queryset = queryset.filter(is_public=True)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return RecipeCreateUpdateSerializer
        return RecipeDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self, request, slug=None):
        """Toggle recipe favorite status"""
        recipe = self.get_object()
        
        if request.user.favorite_recipes.filter(id=recipe.id).exists():
            request.user.favorite_recipes.remove(recipe)
            return Response({'status': 'removed from favorites'})
        else:
            request.user.favorite_recipes.add(recipe)
            return Response({'status': 'added to favorites'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_recipes(self, request):
        """Get current user's recipes"""
        queryset = Recipe.objects.filter(author=request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def favorites(self, request):
        """Get user's favorite recipes"""
        queryset = request.user.favorite_recipes.all()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """API endpoint for reviews"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Review.objects.select_related('user', 'recipe')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
