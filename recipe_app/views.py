from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, Ingredients, Favorites, Rating
from django.http import Http404
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
    ingredients = recipe.ingredients.all()
    ratings = recipe.ratings.all()
    context = {'recipe':recipe, 'ingredients':ingredients, 'ratings':ratings}
    return render(request, 'recipe_app/recipe_detail.html', context)

# Add recipe view
def add_recipe(request):
    if request.method != 'POST':
        recipe_form = RecipeForm()
        return None
    else:
        recipe_form = RecipeForm(data=request.POST)
        if recipe_form.is_valid():
            new_recipe = recipe_form.save(commit=False)
            new_recipe.owner = request.user
            new_recipe.save()
            return redirect('') #redirect to appropriate url
    context = {'form':recipe_form}
    return render(request,'recipe_app/add_recipe.html',context)

# Edit recipe view
def edit_recipe(request, recipe_id):
    #EDIT INGREDIENTS WHERE?
    check_owner(recipe.owner, request.user)
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method != 'POST':
        form = RecipeForm(instance = recipe)
    else:
        form = RecipeForm(instance = review, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('') #redirect to appropriate url
    context = {'recipe':recipe, 'form':form}
    return render(request,'recipe_app/edit_recipe.html',context)

# Add rating view
def add_rating(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method != 'POST':
        form = RatingForm()
    else:
        form = RatingForm(data=request.POST)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.recipe = recipe
            new_recipe.save()
            return redirect('recipe_app:recipe',recipe_id=recipe_id)
    context = {'recipe':recipe,'form':form}
    return render(request,'recipe_app/add_rating.html',context)

# Add to favorites view
# User favorite recipes
def testview(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'recipe_app/test.html', context)

def check_owner(owner, user):
    if owner != user:
        raise Http404