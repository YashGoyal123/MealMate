"""
Forms for Recipes App
"""
from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient, Instruction, Review


class RecipeForm(forms.ModelForm):
    """Form for creating and updating recipes"""
    
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'image', 'video', 'category', 'dietary_tags',
            'prep_time', 'cook_time', 'servings', 'difficulty',
            'calories', 'protein', 'carbohydrates', 'fat', 'fiber', 'is_public'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipe title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your recipe'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'dietary_tags': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '8'}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Per serving'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Grams', 'step': '0.1'}),
            'carbohydrates': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Grams', 'step': '0.1'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Grams', 'step': '0.1'}),
            'fiber': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Grams', 'step': '0.1'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class IngredientForm(forms.ModelForm):
    """Form for recipe ingredients"""
    
    class Meta:
        model = Ingredient
        fields = ['name', 'amount', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingredient name'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2 cups'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# Formset for managing multiple ingredients
IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=3,
    can_delete=True
)


class InstructionForm(forms.ModelForm):
    """Form for recipe instructions"""
    
    class Meta:
        model = Instruction
        fields = ['step_number', 'description', 'image']
        widgets = {
            'step_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


# Formset for managing multiple instructions
InstructionFormSet = inlineformset_factory(
    Recipe,
    Instruction,
    form=InstructionForm,
    extra=3,
    can_delete=True
)


class ReviewForm(forms.ModelForm):
    """Form for recipe reviews"""
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i}★') for i in range(1, 6)], attrs={'class': 'form-check-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your thoughts...'}),
        }
