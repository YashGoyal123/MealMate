"""
Shopping List Models for MealMate
"""
from django.db import models
from django.conf import settings


class ShoppingList(models.Model):
    """Shopping list for a user"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shopping_lists'
    )
    meal_plan = models.ForeignKey(
        'mealplans.MealPlan',
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        null=True,
        blank=True,
        help_text="Optional: Link to meal plan"
    )
    
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    
    # Sharing
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='shared_shopping_lists',
        blank=True,
        help_text="Users this shopping list is shared with"
    )
    
    # Status
    is_completed = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Shopping List'
        verbose_name_plural = 'Shopping Lists'
    
    def __str__(self):
        return self.name
    
    @property
    def total_items(self):
        """Return total number of items"""
        return self.items.count()
    
    @property
    def completed_items(self):
        """Return number of completed items"""
        return self.items.filter(is_purchased=True).count()
    
    @property
    def completion_percentage(self):
        """Calculate completion percentage"""
        if self.total_items == 0:
            return 0
        return int((self.completed_items / self.total_items) * 100)


class ShoppingListItem(models.Model):
    """Individual item in a shopping list"""
    
    CATEGORY_CHOICES = [
        ('produce', 'Produce'),
        ('meat', 'Meat & Seafood'),
        ('dairy', 'Dairy & Eggs'),
        ('bakery', 'Bakery'),
        ('pantry', 'Pantry'),
        ('frozen', 'Frozen'),
        ('beverages', 'Beverages'),
        ('snacks', 'Snacks'),
        ('other', 'Other'),
    ]
    
    shopping_list = models.ForeignKey(
        ShoppingList,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=50, help_text="e.g., 2 lbs, 1 cup")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    
    # Status
    is_purchased = models.BooleanField(default=False)
    
    # Priority
    is_priority = models.BooleanField(
        default=False,
        help_text="Mark as priority item"
    )
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Order
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['is_purchased', 'category', 'order', 'name']
        verbose_name = 'Shopping List Item'
        verbose_name_plural = 'Shopping List Items'
    
    def __str__(self):
        return f"{self.quantity} {self.name}"
