"""
URL Configuration for Recipes App
"""
from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Recipe CRUD
    path('', views.RecipeListView.as_view(), name='recipe_list'),
    path('my-recipes/', views.MyRecipesView.as_view(), name='my_recipes'),
    path('favorites/', views.FavoriteRecipesView.as_view(), name='favorites'),
    path('create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('<slug:slug>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('<slug:slug>/edit/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('<slug:slug>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
    
    # Actions
    path('<slug:slug>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<slug:slug>/review/', views.add_review, name='add_review'),
    path('<slug:slug>/review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<slug:slug>/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('<slug:slug>/review/<int:review_id>/reply/', views.reply_to_review, name='reply_to_review'),
    path('<slug:slug>/review/<int:review_id>/reply/delete/', views.delete_reply, name='delete_reply'),
]
