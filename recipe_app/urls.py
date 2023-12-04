# Recipe app urls
from django.urls import path
from . import views

app_name = 'recipe_app'

urlpatterns = [
    # Main page, using same naming as in the book
    path('', views.index, name='index'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipe/<int:recipe_id>', views.recipe_detail, name='recipe_detail'),
    path('testing/', views.testview, name='test'),
]