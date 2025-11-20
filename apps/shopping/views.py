"""
Views for Shopping App
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import ShoppingList, ShoppingListItem
from .forms import ShoppingListForm, ShoppingListItemForm
from apps.mealplans.models import MealPlan
from apps.recipes.models import Recipe


class ShoppingListListView(LoginRequiredMixin, ListView):
    """List user's shopping lists"""
    model = ShoppingList
    template_name = 'shopping/shoppinglist_list.html'
    context_object_name = 'shopping_lists'
    paginate_by = 10
    
    def get_queryset(self):
        # Return only owned lists for pagination
        return ShoppingList.objects.filter(
            user=self.request.user
        ).prefetch_related('items', 'shared_with')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add shared lists separately
        context['shared_shopping_lists'] = ShoppingList.objects.filter(
            shared_with=self.request.user
        ).exclude(user=self.request.user).prefetch_related('items', 'shared_with', 'user')
        return context


class ShoppingListDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a shopping list"""
    model = ShoppingList
    template_name = 'shopping/shoppinglist_detail.html'
    context_object_name = 'shopping_list'
    
    def get_queryset(self):
        from django.db.models import Q
        # Include both owned and shared lists
        return ShoppingList.objects.filter(
            Q(user=self.request.user) | Q(shared_with=self.request.user)
        ).distinct().prefetch_related('items', 'shared_with')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_list = self.object
        
        # Organize items by source (recipe name from notes) or category
        items_by_category = {}
        for item in shopping_list.items.all():
            # If notes contain "From [Recipe Name]", use that as the category
            if item.notes and item.notes.startswith('From '):
                category = item.notes.replace('From ', '')
            else:
                category = item.get_category_display()
            
            if category not in items_by_category:
                items_by_category[category] = []
            items_by_category[category].append(item)
        
        context['items_by_category'] = items_by_category
        return context


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    """Create a new shopping list"""
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'shopping/shoppinglist_form.html'
    success_url = reverse_lazy('shopping:shoppinglist_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Shopping list created successfully!')
        return super().form_valid(form)


class ShoppingListUpdateView(LoginRequiredMixin, UpdateView):
    """Update a shopping list"""
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'shopping/shoppinglist_form.html'
    
    def get_queryset(self):
        # Only owner can edit list details
        return ShoppingList.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        """Check if user is trying to edit a shared list"""
        from django.db.models import Q
        pk = self.kwargs.get('pk')
        shared_list = ShoppingList.objects.filter(
            pk=pk,
            shared_with=request.user
        ).first()
        
        if shared_list:
            messages.error(request, 'You cannot edit this list. Only the owner can edit list details.')
            return redirect('shopping:shoppinglist_detail', pk=pk)
        
        return super().get(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('shopping:shoppinglist_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Shopping list updated successfully!')
        return super().form_valid(form)


class ShoppingListDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a shopping list"""
    model = ShoppingList
    template_name = 'shopping/shoppinglist_confirm_delete.html'
    success_url = reverse_lazy('shopping:shoppinglist_list')
    
    def get_queryset(self):
        # Only owner can delete
        return ShoppingList.objects.filter(user=self.request.user)
    
    def get_object(self, queryset=None):
        """Override to provide better error message for shared lists"""
        obj = super().get_object(queryset)
        return obj
    
    def get(self, request, *args, **kwargs):
        """Check if user is trying to delete a shared list"""
        from django.db.models import Q
        pk = self.kwargs.get('pk')
        shared_list = ShoppingList.objects.filter(
            pk=pk,
            shared_with=request.user
        ).first()
        
        if shared_list:
            messages.error(request, 'You cannot delete a shared list. Only the owner can delete it.')
            return redirect('shopping:shoppinglist_detail', pk=pk)
        
        return super().get(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Shopping list deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
def generate_from_meal_plan(request, meal_plan_id):
    """Generate a shopping list from a meal plan"""
    meal_plan = get_object_or_404(MealPlan, pk=meal_plan_id, user=request.user)
    
    # Create shopping list
    shopping_list = ShoppingList.objects.create(
        user=request.user,
        meal_plan=meal_plan,
        name=f"Shopping for {meal_plan.name}"
    )
    
    # Collect ingredients from all meals
    ingredients_dict = {}
    for meal in meal_plan.meals.select_related('recipe').prefetch_related('recipe__ingredients'):
        for ingredient in meal.recipe.ingredients.all():
            key = ingredient.name.lower()
            if key in ingredients_dict:
                # Ingredient already exists, could implement smart merging here
                ingredients_dict[key]['count'] += 1
            else:
                ingredients_dict[key] = {
                    'name': ingredient.name,
                    'amount': ingredient.amount,
                    'count': 1
                }
    
    # Create shopping list items
    for ingredient_data in ingredients_dict.values():
        quantity = f"{ingredient_data['amount']} (x{ingredient_data['count']})" if ingredient_data['count'] > 1 else ingredient_data['amount']
        ShoppingListItem.objects.create(
            shopping_list=shopping_list,
            name=ingredient_data['name'],
            quantity=quantity,
            category='other'  # Could implement smart categorization
        )
    
    messages.success(request, f'Shopping list generated with {len(ingredients_dict)} items!')
    return redirect('shopping:shoppinglist_detail', pk=shopping_list.pk)


@login_required
def add_recipe_to_shopping_list(request, recipe_slug):
    """Add recipe ingredients to a shopping list"""
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    
    if request.method == 'POST':
        shopping_list_id = request.POST.get('shopping_list_id')
        
        if shopping_list_id == 'new':
            # Create new shopping list
            shopping_list = ShoppingList.objects.create(
                user=request.user,
                name=f"Shopping for {recipe.title}"
            )
        else:
            # Use existing shopping list (allow shared lists too)
            from django.db.models import Q
            shopping_list = get_object_or_404(
                ShoppingList.objects.filter(
                    Q(user=request.user) | Q(shared_with=request.user)
                ),
                pk=shopping_list_id
            )
        
        # Add ingredients to shopping list
        ingredients_added = 0
        for ingredient in recipe.ingredients.all():
            # Check if item already exists
            existing_item = shopping_list.items.filter(name__iexact=ingredient.name).first()
            if existing_item:
                # Update quantity if exists
                existing_item.quantity = f"{existing_item.quantity} + {ingredient.amount}"
                existing_item.save()
            else:
                # Create new item
                ShoppingListItem.objects.create(
                    shopping_list=shopping_list,
                    name=ingredient.name,
                    quantity=ingredient.amount,
                    notes=f"From {recipe.title}",
                    category='other'  # Could implement smart categorization
                )
            ingredients_added += 1
        
        messages.success(request, f'Added {ingredients_added} ingredients from "{recipe.title}" to shopping list!')
        return redirect('shopping:shoppinglist_detail', pk=shopping_list.pk)
    
    # GET request: show shopping list selection (include shared lists)
    from django.db.models import Q
    shopping_lists = ShoppingList.objects.filter(
        Q(user=request.user) | Q(shared_with=request.user)
    ).distinct().order_by('-created_at')
    return render(request, 'shopping/add_recipe_to_list.html', {
        'recipe': recipe,
        'shopping_lists': shopping_lists
    })


@login_required
def toggle_item_purchased(request, pk):
    """Toggle shopping list item purchased status"""
    from django.db.models import Q
    # Allow both owner and shared users to toggle items
    item = get_object_or_404(
        ShoppingListItem,
        pk=pk,
        shopping_list__in=ShoppingList.objects.filter(
            Q(user=request.user) | Q(shared_with=request.user)
        )
    )
    item.is_purchased = not item.is_purchased
    item.save()
    return redirect('shopping:shoppinglist_detail', pk=item.shopping_list.pk)


class ShoppingListItemCreateView(LoginRequiredMixin, CreateView):
    """Add an item to a shopping list"""
    model = ShoppingListItem
    form_class = ShoppingListItemForm
    template_name = 'shopping/shoppinglistitem_form.html'
    
    def form_valid(self, form):
        from django.db.models import Q
        # Allow both owner and shared users to add items
        shopping_list = get_object_or_404(
            ShoppingList.objects.filter(
                Q(user=self.request.user) | Q(shared_with=self.request.user)
            ),
            pk=self.kwargs.get('shopping_list_id')
        )
        form.instance.shopping_list = shopping_list
        messages.success(self.request, 'Item added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('shopping:shoppinglist_detail', kwargs={'pk': self.kwargs.get('shopping_list_id')})


class ShoppingListItemUpdateView(LoginRequiredMixin, UpdateView):
    """Update a shopping list item"""
    model = ShoppingListItem
    form_class = ShoppingListItemForm
    template_name = 'shopping/shoppinglistitem_form.html'
    
    def get_queryset(self):
        from django.db.models import Q
        # Allow both owner and shared users to edit items
        return ShoppingListItem.objects.filter(
            Q(shopping_list__user=self.request.user) | Q(shopping_list__shared_with=self.request.user)
        )
    
    def get_success_url(self):
        return reverse_lazy('shopping:shoppinglist_detail', kwargs={'pk': self.object.shopping_list.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Item updated successfully!')
        return super().form_valid(form)


class ShoppingListItemDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a shopping list item"""
    model = ShoppingListItem
    template_name = 'shopping/shoppinglistitem_confirm_delete.html'
    
    def get_queryset(self):
        from django.db.models import Q
        # Allow both owner and shared users to delete items
        return ShoppingListItem.objects.filter(
            Q(shopping_list__user=self.request.user) | Q(shopping_list__shared_with=self.request.user)
        )
    
    def get_success_url(self):
        return reverse_lazy('shopping:shoppinglist_detail', kwargs={'pk': self.object.shopping_list.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Item removed successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
def share_shopping_list(request, pk):
    """Share a shopping list with another user"""
    shopping_list = get_object_or_404(ShoppingList, pk=pk, user=request.user)
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        
        if username:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            try:
                user_to_share = User.objects.get(username=username)
                
                if user_to_share == request.user:
                    messages.error(request, 'You cannot share a list with yourself.')
                elif shopping_list.shared_with.filter(id=user_to_share.id).exists():
                    messages.warning(request, f'List is already shared with {username}.')
                else:
                    shopping_list.shared_with.add(user_to_share)
                    messages.success(request, f'Shopping list shared with {username} successfully!')
            except User.DoesNotExist:
                messages.error(request, f'User "{username}" not found.')
        else:
            messages.error(request, 'Please enter a username.')
    
    return redirect('shopping:shoppinglist_detail', pk=pk)


@login_required
def unshare_shopping_list(request, pk, user_id):
    """Remove user access from a shared shopping list"""
    shopping_list = get_object_or_404(ShoppingList, pk=pk, user=request.user)
    
    if request.method == 'POST':
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user_to_remove = get_object_or_404(User, id=user_id)
        shopping_list.shared_with.remove(user_to_remove)
        messages.success(request, f'Stopped sharing with {user_to_remove.username}.')
    
    return redirect('shopping:shoppinglist_detail', pk=pk)


@login_required
def leave_shared_list(request, pk):
    """Allow a shared user to remove themselves from a shopping list"""
    shopping_list = get_object_or_404(ShoppingList, pk=pk, shared_with=request.user)
    
    if request.method == 'POST':
        shopping_list.shared_with.remove(request.user)
        messages.success(request, f'Shopping list "{shopping_list.name}" removed successfully!')
        return redirect('shopping:shoppinglist_list')
    
    return redirect('shopping:shoppinglist_detail', pk=pk)
