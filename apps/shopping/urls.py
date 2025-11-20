"""
URL Configuration for Shopping App
"""
from django.urls import path
from . import views

app_name = 'shopping'

urlpatterns = [
    # Shopping List CRUD
    path('', views.ShoppingListListView.as_view(), name='shoppinglist_list'),
    path('create/', views.ShoppingListCreateView.as_view(), name='shoppinglist_create'),
    path('<int:pk>/', views.ShoppingListDetailView.as_view(), name='shoppinglist_detail'),
    path('<int:pk>/edit/', views.ShoppingListUpdateView.as_view(), name='shoppinglist_update'),
    path('<int:pk>/delete/', views.ShoppingListDeleteView.as_view(), name='shoppinglist_delete'),
    
    # Generate from meal plan
    path('generate/<int:meal_plan_id>/', views.generate_from_meal_plan, name='generate_from_meal_plan'),
    
    # Add recipe to shopping list
    path('add-recipe/<slug:recipe_slug>/', views.add_recipe_to_shopping_list, name='add_recipe_to_list'),
    
    # Shopping List Item CRUD
    path('<int:shopping_list_id>/add-item/', views.ShoppingListItemCreateView.as_view(), name='item_create'),
    path('item/<int:pk>/edit/', views.ShoppingListItemUpdateView.as_view(), name='item_update'),
    path('item/<int:pk>/delete/', views.ShoppingListItemDeleteView.as_view(), name='item_delete'),
    path('item/<int:pk>/toggle/', views.toggle_item_purchased, name='toggle_item_purchased'),
    
    # Sharing
    path('<int:pk>/share/', views.share_shopping_list, name='share_list'),
    path('<int:pk>/unshare/<int:user_id>/', views.unshare_shopping_list, name='unshare_list'),
    path('<int:pk>/leave/', views.leave_shared_list, name='leave_list'),
]
