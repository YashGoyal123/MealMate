"""
Admin Configuration for Recipes App
"""
from django.contrib import admin
from .models import Category, DietaryTag, Recipe, Ingredient, Instruction, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model"""
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(DietaryTag)
class DietaryTagAdmin(admin.ModelAdmin):
    """Admin configuration for DietaryTag model"""
    list_display = ['name', 'slug', 'color', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


class IngredientInline(admin.TabularInline):
    """Inline admin for ingredients"""
    model = Ingredient
    extra = 3


class InstructionInline(admin.StackedInline):
    """Inline admin for instructions"""
    model = Instruction
    extra = 3


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin configuration for Recipe model"""
    list_display = ['title', 'author', 'category', 'difficulty', 'prep_time', 'cook_time', 'is_public', 'created_at']
    list_filter = ['category', 'difficulty', 'is_public', 'created_at', 'dietary_tags']
    search_fields = ['title', 'description', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['slug', 'views', 'created_at', 'updated_at']
    filter_horizontal = ['dietary_tags']
    inlines = [IngredientInline, InstructionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'author', 'image')
        }),
        ('Categorization', {
            'fields': ('category', 'dietary_tags')
        }),
        ('Cooking Details', {
            'fields': ('prep_time', 'cook_time', 'servings', 'difficulty')
        }),
        ('Nutrition', {
            'fields': ('calories', 'protein', 'carbohydrates', 'fat', 'fiber'),
            'classes': ('collapse',)
        }),
        ('Visibility & Stats', {
            'fields': ('is_public', 'views')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for Review model"""
    list_display = ['recipe', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['recipe__title', 'user__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        # If editing an existing review, make user content read-only
        if obj:  # Editing existing review
            return ['user', 'recipe', 'rating', 'comment', 'reply', 'created_at', 'updated_at']
        # If adding a new review, only timestamps are read-only
        return ['created_at', 'updated_at']
    
    def has_change_permission(self, request, obj=None):
        # Admins cannot change existing reviews
        return False
