"""
Meal Plan Models for MealMate
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class MealPlan(models.Model):
    """Weekly meal plan"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meal_plans'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Date range
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Meal Plan'
        verbose_name_plural = 'Meal Plans'
        indexes = [
            models.Index(fields=['user', '-start_date']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"
    
    def save(self, *args, **kwargs):
        # Auto-set end_date to 7 days from start_date if not provided
        if not self.end_date and self.start_date:
            self.end_date = self.start_date + timedelta(days=6)
        super().save(*args, **kwargs)
    
    @property
    def total_recipes(self):
        """Return the total number of recipes in this meal plan"""
        return self.meals.count()
    
    @property
    def is_current(self):
        """Check if the meal plan is currently active"""
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


class Meal(models.Model):
    """Individual meal within a meal plan"""
    
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    meal_plan = models.ForeignKey(
        MealPlan,
        on_delete=models.CASCADE,
        related_name='meals'
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='planned_meals'
    )
    
    # Meal details
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    date = models.DateField()
    
    # Servings adjustment
    servings = models.PositiveIntegerField(
        default=1,
        help_text="Number of servings for this meal"
    )
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Status
    is_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'meal_type']
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'
        indexes = [
            models.Index(fields=['meal_plan', 'date']),
        ]
    
    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.recipe.title} ({self.date})"
    
    @property
    def total_calories(self):
        """Calculate total calories for this meal based on servings"""
        if self.recipe.calories:
            return self.recipe.calories * self.servings
        return None
