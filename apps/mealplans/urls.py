"""
URL Configuration for Meal Plans App
"""
from django.urls import path
from . import views

app_name = 'mealplans'

urlpatterns = [
    # Meal Plan CRUD
    path('', views.MealPlanListView.as_view(), name='mealplan_list'),
    path('create/', views.MealPlanCreateView.as_view(), name='mealplan_create'),
    path('<int:pk>/', views.MealPlanDetailView.as_view(), name='mealplan_detail'),
    path('<int:pk>/edit/', views.MealPlanUpdateView.as_view(), name='mealplan_update'),
    path('<int:pk>/delete/', views.MealPlanDeleteView.as_view(), name='mealplan_delete'),
    
    # Meal CRUD
    path('<int:meal_plan_id>/add-meal/', views.MealCreateView.as_view(), name='meal_create'),
    path('meal/<int:pk>/edit/', views.MealUpdateView.as_view(), name='meal_update'),
    path('meal/<int:pk>/delete/', views.MealDeleteView.as_view(), name='meal_delete'),
]
