"""
Admin Configuration for Meal Plans App
"""
from django.contrib import admin
from .models import MealPlan, Meal


class MealInline(admin.TabularInline):
    """Inline admin for meals"""
    model = Meal
    extra = 1
    autocomplete_fields = ['recipe']


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    """Admin configuration for MealPlan model"""
    list_display = ['name', 'user', 'start_date', 'end_date', 'is_active', 'total_recipes', 'created_at']
    list_filter = ['is_active', 'start_date', 'created_at']
    search_fields = ['name', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [MealInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'description')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
