"""
REST API Serializers for Recipes App
"""
from rest_framework import serializers
from .models import Category, DietaryTag, Recipe, Ingredient, Instruction, Review


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    recipe_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'recipe_count', 'created_at']
        read_only_fields = ['slug', 'created_at']
    
    def get_recipe_count(self, obj):
        return obj.recipes.count()


class DietaryTagSerializer(serializers.ModelSerializer):
    """Serializer for DietaryTag model"""
    
    class Meta:
        model = DietaryTag
        fields = ['id', 'name', 'slug', 'description', 'color', 'created_at']
        read_only_fields = ['slug', 'created_at']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model"""
    
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'amount', 'order']


class InstructionSerializer(serializers.ModelSerializer):
    """Serializer for Instruction model"""
    
    class Meta:
        model = Instruction
        fields = ['id', 'step_number', 'description', 'image']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'recipe', 'user', 'user_username', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class RecipeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for recipe lists"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    dietary_tags = DietaryTagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'slug', 'description', 'author', 'author_username',
            'image', 'category', 'category_name', 'dietary_tags',
            'prep_time', 'cook_time', 'total_time', 'servings', 'difficulty',
            'calories', 'is_public', 'views', 'favorite_count', 'created_at'
        ]
        read_only_fields = ['slug', 'author', 'views', 'created_at']


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual recipe view"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    dietary_tags = DietaryTagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    instructions = InstructionSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'slug', 'description', 'author', 'author_username',
            'image', 'category', 'category_name', 'dietary_tags',
            'prep_time', 'cook_time', 'total_time', 'servings', 'difficulty',
            'calories', 'protein', 'carbohydrates', 'fat', 'fiber',
            'is_public', 'views', 'favorite_count',
            'ingredients', 'instructions', 'reviews',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'author', 'views', 'created_at', 'updated_at']


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating recipes"""
    ingredients = IngredientSerializer(many=True, required=False)
    instructions = InstructionSerializer(many=True, required=False)
    
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'image', 'category', 'dietary_tags',
            'prep_time', 'cook_time', 'servings', 'difficulty',
            'calories', 'protein', 'carbohydrates', 'fat', 'fiber',
            'is_public', 'ingredients', 'instructions'
        ]
    
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        instructions_data = validated_data.pop('instructions', [])
        dietary_tags = validated_data.pop('dietary_tags', [])
        
        recipe = Recipe.objects.create(**validated_data)
        recipe.dietary_tags.set(dietary_tags)
        
        # Create ingredients
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        
        # Create instructions
        for instruction_data in instructions_data:
            Instruction.objects.create(recipe=recipe, **instruction_data)
        
        return recipe
    
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        instructions_data = validated_data.pop('instructions', None)
        dietary_tags = validated_data.pop('dietary_tags', None)
        
        # Update recipe fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update dietary tags
        if dietary_tags is not None:
            instance.dietary_tags.set(dietary_tags)
        
        # Update ingredients
        if ingredients_data is not None:
            instance.ingredients.all().delete()
            for ingredient_data in ingredients_data:
                Ingredient.objects.create(recipe=instance, **ingredient_data)
        
        # Update instructions
        if instructions_data is not None:
            instance.instructions.all().delete()
            for instruction_data in instructions_data:
                Instruction.objects.create(recipe=instance, **instruction_data)
        
        return instance
