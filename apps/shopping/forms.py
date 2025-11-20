"""
Forms for Shopping App
"""
from django import forms
from .models import ShoppingList, ShoppingListItem
from apps.mealplans.models import MealPlan


class ShoppingListForm(forms.ModelForm):
    """Form for creating and updating shopping lists"""
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = ShoppingList
        fields = ['name', 'notes', 'is_completed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Weekly Groceries'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'List Name',
            'notes': 'Notes',
            'is_completed': 'Mark as completed',
        }


class ShoppingListItemForm(forms.ModelForm):
    """Form for adding items to a shopping list"""
    
    class Meta:
        model = ShoppingListItem
        fields = ['name', 'quantity', 'category', 'is_priority', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item name'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2 lbs'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_priority': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional notes'}),
        }
