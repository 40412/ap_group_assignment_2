# Recipe app urls
from django.urls import path
from . import views

app_name = 'recipe_app'

urlpatterns = [
    # Main page, using same naming as in the book
    path('', views.index, name='index'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/<int:recipe_id>', views.recipe_detail, name='recipe_detail'),
    path('user/', views.profile, name='profile'),
    path('toggle-favorite/<int:recipe_id>/', views.toggle_favorite, name='toggle-favorite'),
    path('new-rating/<int:recipe_id>/', views.add_rating, name='new_rating'),
    path('new-recipe/', views.add_recipe, name='new_recipe'),
    path('testing/', views.testview, name='test'),
    path('edit-recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]
