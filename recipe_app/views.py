from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, Ingredients, Favorites, Rating
# Create your views here.

# Main page
def index(request):
    return render(request, 'recipe_app/index.html')

# Display all recipes
def recipes(request): # + sort type
    recipes = Recipe.objects.order_by('date_added') #sort by popularity?
    context = {'recipes':recipes}
    return render(request, 'recipe_app/all_recipes.html', context)

# Detailed recipe view
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = recipe.Ingredients.get()
    ratings = recipe.ratings.all()
    context = {'recipe':recipe, 'ingredients':ingredients, 'ratings':ratings}
    return render(request, 'recipe_app/recipe_detail.html', context)
# Add recipe view
# Edit recipe view
# Add rating view
# Add to favorites view
# User favorite recipes
def testview(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'recipe_app/test.html', context)