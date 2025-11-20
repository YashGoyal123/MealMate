"""
Admin Configuration for Shopping App
"""
from django.contrib import admin
from .models import ShoppingList, ShoppingListItem


class ShoppingListItemInline(admin.TabularInline):
    """Inline admin for shopping list items"""
    model = ShoppingListItem
    extra = 3


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Admin configuration for ShoppingList model"""
    list_display = ['name', 'user', 'meal_plan', 'total_items', 'completed_items', 'completion_percentage', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['name', 'user__username', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['meal_plan']
    inlines = [ShoppingListItemInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'meal_plan', 'name', 'notes')
        }),
        ('Status', {
            'fields': ('is_completed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
