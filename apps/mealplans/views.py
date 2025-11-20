"""
Views for Meal Plans App
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime, timedelta

from .models import MealPlan, Meal
from .forms import MealPlanForm, MealForm


class MealPlanListView(LoginRequiredMixin, ListView):
    """List user's meal plans"""
    model = MealPlan
    template_name = 'mealplans/mealplan_list.html'
    context_object_name = 'meal_plans'
    paginate_by = 10
    
    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user).prefetch_related('meals__recipe')


class MealPlanDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a meal plan"""
    model = MealPlan
    template_name = 'mealplans/mealplan_detail.html'
    context_object_name = 'meal_plan'
    
    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user).prefetch_related(
            'meals__recipe__dietary_tags'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meal_plan = self.object
        
        # Organize meals by day and type
        meals_by_day = {}
        for day in range(7):
            day_date = meal_plan.start_date + timedelta(days=day)
            meals_by_day[day] = {
                'date': day_date,
                'day_name': day_date.strftime('%A'),
                'meals': {
                    'breakfast': meal_plan.meals.filter(day_of_week=day, meal_type='breakfast').first(),
                    'lunch': meal_plan.meals.filter(day_of_week=day, meal_type='lunch').first(),
                    'dinner': meal_plan.meals.filter(day_of_week=day, meal_type='dinner').first(),
                    'snack': meal_plan.meals.filter(day_of_week=day, meal_type='snack').first(),
                }
            }
        
        context['meals_by_day'] = meals_by_day
        return context


class MealPlanCreateView(LoginRequiredMixin, CreateView):
    """Create a new meal plan"""
    model = MealPlan
    form_class = MealPlanForm
    template_name = 'mealplans/mealplan_form.html'
    success_url = reverse_lazy('mealplans:mealplan_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Meal plan created successfully!')
        return super().form_valid(form)


class MealPlanUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing meal plan"""
    model = MealPlan
    form_class = MealPlanForm
    template_name = 'mealplans/mealplan_form.html'
    
    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('mealplans:mealplan_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Meal plan updated successfully!')
        return super().form_valid(form)


class MealPlanDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a meal plan"""
    model = MealPlan
    template_name = 'mealplans/mealplan_confirm_delete.html'
    success_url = reverse_lazy('mealplans:mealplan_list')
    
    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Meal plan deleted successfully!')
        return super().delete(request, *args, **kwargs)


class MealCreateView(LoginRequiredMixin, CreateView):
    """Add a meal to a meal plan"""
    model = Meal
    form_class = MealForm
    template_name = 'mealplans/meal_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        
        # Get meal_plan and pass it to the form
        meal_plan = get_object_or_404(
            MealPlan,
            pk=self.kwargs.get('meal_plan_id'),
            user=self.request.user
        )
        kwargs['meal_plan'] = meal_plan
        
        # Set initial values from query params if provided
        initial = kwargs.get('initial', {})
        if 'day' in self.request.GET:
            initial['day_of_week'] = self.request.GET.get('day')
        if 'type' in self.request.GET:
            initial['meal_type'] = self.request.GET.get('type')
        kwargs['initial'] = initial
        
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meal_plan = get_object_or_404(
            MealPlan,
            pk=self.kwargs.get('meal_plan_id'),
            user=self.request.user
        )
        context['meal_plan'] = meal_plan
        return context
    
    def form_valid(self, form):
        meal_plan = get_object_or_404(
            MealPlan,
            pk=self.kwargs.get('meal_plan_id'),
            user=self.request.user
        )
        form.instance.meal_plan = meal_plan
        messages.success(self.request, 'Meal added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('mealplans:mealplan_detail', kwargs={'pk': self.kwargs.get('meal_plan_id')})


class MealUpdateView(LoginRequiredMixin, UpdateView):
    """Update a meal in a meal plan"""
    model = Meal
    form_class = MealForm
    template_name = 'mealplans/meal_form.html'
    
    def get_queryset(self):
        return Meal.objects.filter(meal_plan__user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('mealplans:mealplan_detail', kwargs={'pk': self.object.meal_plan.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Meal updated successfully!')
        return super().form_valid(form)


class MealDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a meal from a meal plan"""
    model = Meal
    template_name = 'mealplans/meal_confirm_delete.html'
    
    def get_queryset(self):
        return Meal.objects.filter(meal_plan__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('mealplans:mealplan_detail', kwargs={'pk': self.object.meal_plan.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Meal removed successfully!')
        return super().delete(request, *args, **kwargs)
