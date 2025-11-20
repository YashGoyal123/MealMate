"""
Forms for Meal Plans App
"""
from django import forms
from django.db.models import Q
from .models import MealPlan, Meal
from apps.recipes.models import Recipe


class MealPlanForm(forms.ModelForm):
    """Form for creating and updating meal plans"""
    
    class Meta:
        model = MealPlan
        fields = ['name', 'description', 'start_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Week of Jan 1-7',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Optional description (e.g., Low carb meals, Family favorites)'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date',
                'required': True
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default value for start_date to today if not editing
        if not self.instance.pk:
            from datetime import date
            self.initial['start_date'] = date.today()
            self.initial['is_active'] = True


class MealForm(forms.ModelForm):
    """Form for adding meals to a meal plan"""
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        meal_plan = kwargs.pop('meal_plan', None)
        super().__init__(*args, **kwargs)
        
        # Filter recipes to show user's recipes and public recipes
        if user:
            self.fields['recipe'].queryset = Recipe.objects.filter(
                Q(author=user) | Q(is_public=True)
            ).select_related('category')
        
        # Store meal_plan for date calculation
        self.meal_plan = meal_plan
        
        # Hide date field as it will be auto-calculated
        self.fields['date'].required = False
        self.fields['date'].widget = forms.HiddenInput()
    
    def clean(self):
        cleaned_data = super().clean()
        day_of_week = cleaned_data.get('day_of_week')
        
        # Auto-calculate date from meal_plan start_date and day_of_week
        if self.meal_plan and day_of_week is not None:
            from datetime import timedelta
            cleaned_data['date'] = self.meal_plan.start_date + timedelta(days=day_of_week)
        
        return cleaned_data
    
    class Meta:
        model = Meal
        fields = ['recipe', 'meal_type', 'day_of_week', 'date', 'servings', 'notes']
        widgets = {
            'recipe': forms.Select(attrs={'class': 'form-select'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional notes'}),
        }

