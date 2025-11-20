"""
Views for Recipes App
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg
from django.contrib import messages

from .models import Recipe, Category, DietaryTag, Ingredient, Instruction, Review
from .forms import RecipeForm, IngredientFormSet, InstructionFormSet, ReviewForm


class DashboardView(LoginRequiredMixin, ListView):
    """User dashboard showing their recipes and meal plans"""
    model = Recipe
    template_name = 'recipes/dashboard.html'
    context_object_name = 'user_recipes'
    
    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user).select_related('category')[:6]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['total_recipes'] = user.recipes.count()
        context['total_meal_plans'] = user.meal_plans.count()
        context['favorite_recipes'] = user.favorite_recipes.all()[:6]
        return context


class RecipeListView(LoginRequiredMixin, ListView):
    """List all public recipes"""
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Recipe.objects.filter(is_public=True).select_related(
            'author', 'category'
        ).prefetch_related('dietary_tags')
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(ingredients__name__icontains=search)
            ).distinct()
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by dietary tags
        dietary_tag = self.request.GET.get('dietary_tag')
        if dietary_tag:
            queryset = queryset.filter(dietary_tags__slug=dietary_tag)
        
        # Filter by difficulty
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by max calories
        max_calories = self.request.GET.get('max_calories')
        if max_calories:
            queryset = queryset.filter(calories__lte=int(max_calories))
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['dietary_tags'] = DietaryTag.objects.all()
        context['difficulties'] = Recipe.DIFFICULTY_CHOICES
        return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a single recipe"""
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Show public recipes or user's own recipes
        queryset = Recipe.objects.select_related('author', 'category').prefetch_related(
            'dietary_tags', 'ingredients', 'instructions', 'reviews__user'
        )
        if self.request.user.is_authenticated:
            return queryset.filter(Q(is_public=True) | Q(author=self.request.user))
        return queryset.filter(is_public=True)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment views
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object
        
        # Check if user has favorited this recipe
        if self.request.user.is_authenticated:
            context['is_favorited'] = self.request.user.favorite_recipes.filter(id=recipe.id).exists()
            context['user_review'] = recipe.reviews.filter(user=self.request.user).first()
        
        # Calculate average rating
        avg_rating = recipe.reviews.aggregate(Avg('rating'))['rating__avg']
        context['avg_rating'] = round(avg_rating, 1) if avg_rating else None
        context['review_count'] = recipe.reviews.count()
        
        context['review_form'] = ReviewForm()
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Create a new recipe"""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = IngredientFormSet(self.request.POST, prefix='ingredients')
            context['instruction_formset'] = InstructionFormSet(self.request.POST, self.request.FILES, prefix='instructions')
        else:
            context['ingredient_formset'] = IngredientFormSet(prefix='ingredients')
            context['instruction_formset'] = InstructionFormSet(prefix='instructions')
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        instruction_formset = context['instruction_formset']
        
        if ingredient_formset.is_valid() and instruction_formset.is_valid():
            form.instance.author = self.request.user
            self.object = form.save()
            
            # Save ingredients
            ingredient_formset.instance = self.object
            ingredient_formset.save()
            
            # Save instructions
            instruction_formset.instance = self.object
            instruction_formset.save()
            
            messages.success(self.request, 'Recipe created successfully!')
            return redirect(self.object.get_absolute_url())
        else:
            return self.form_invalid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing recipe"""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Only allow users to edit their own recipes
        return Recipe.objects.filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = IngredientFormSet(
                self.request.POST,
                instance=self.object,
                prefix='ingredients'
            )
            context['instruction_formset'] = InstructionFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
                prefix='instructions'
            )
        else:
            context['ingredient_formset'] = IngredientFormSet(instance=self.object, prefix='ingredients')
            context['instruction_formset'] = InstructionFormSet(instance=self.object, prefix='instructions')
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        instruction_formset = context['instruction_formset']
        
        if ingredient_formset.is_valid() and instruction_formset.is_valid():
            self.object = form.save()
            ingredient_formset.save()
            instruction_formset.save()
            messages.success(self.request, 'Recipe updated successfully!')
            return redirect(self.object.get_absolute_url())
        else:
            return self.form_invalid(form)


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a recipe"""
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipes:dashboard')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Only allow users to delete their own recipes
        return Recipe.objects.filter(author=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recipe deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
def toggle_favorite(request, slug):
    """Toggle recipe favorite status"""
    recipe = get_object_or_404(Recipe, slug=slug)
    
    if request.user.favorite_recipes.filter(id=recipe.id).exists():
        request.user.favorite_recipes.remove(recipe)
        messages.info(request, f'Removed {recipe.title} from favorites.')
    else:
        request.user.favorite_recipes.add(recipe)
        messages.success(request, f'Added {recipe.title} to favorites!')
    
    return redirect('recipes:recipe_detail', slug=slug)


@login_required
def add_review(request, slug):
    """Add a review to a recipe"""
    recipe = get_object_or_404(Recipe, slug=slug)
    
    # Prevent authors from reviewing their own recipes
    if request.user == recipe.author:
        messages.error(request, 'You cannot review your own recipe.')
        return redirect('recipes:recipe_detail', slug=slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
        else:
            messages.error(request, 'Error adding review.')
    
    return redirect('recipes:recipe_detail', slug=slug)


@login_required
def edit_review(request, slug, review_id):
    """Edit a review"""
    recipe = get_object_or_404(Recipe, slug=slug)
    review = get_object_or_404(Review, id=review_id, user=request.user, recipe=recipe)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
        else:
            messages.error(request, 'Error updating review.')
    
    return redirect('recipes:recipe_detail', slug=slug)


@login_required
def delete_review(request, slug, review_id):
    """Delete a review"""
    recipe = get_object_or_404(Recipe, slug=slug)
    review = get_object_or_404(Review, id=review_id, user=request.user, recipe=recipe)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
    
    return redirect('recipes:recipe_detail', slug=slug)


@login_required
def reply_to_review(request, slug, review_id):
    """Reply to a review (only recipe author can reply)"""
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)
    review = get_object_or_404(Review, id=review_id, recipe=recipe)
    
    if request.method == 'POST':
        reply_text = request.POST.get('reply', '').strip()
        if reply_text:
            review.reply = reply_text
            review.save()
            messages.success(request, 'Reply added successfully!')
        else:
            messages.error(request, 'Reply cannot be empty.')
    
    return redirect('recipes:recipe_detail', slug=slug)


@login_required
def delete_reply(request, slug, review_id):
    """Delete a reply (only recipe author can delete)"""
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)
    review = get_object_or_404(Review, id=review_id, recipe=recipe)
    
    if request.method == 'POST':
        review.reply = ''
        review.save()
        messages.success(request, 'Reply deleted successfully!')
    
    return redirect('recipes:recipe_detail', slug=slug)


class MyRecipesView(LoginRequiredMixin, ListView):
    """List user's own recipes"""
    model = Recipe
    template_name = 'recipes/my_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user).select_related('category')


class FavoriteRecipesView(LoginRequiredMixin, ListView):
    """List user's favorite recipes"""
    model = Recipe
    template_name = 'recipes/favorite_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        return self.request.user.favorite_recipes.all().select_related('author', 'category')
