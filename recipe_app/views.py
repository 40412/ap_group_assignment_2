from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe, Ingredients, Favorites, Rating
from django.http import Http404, JsonResponse
from .forms import RecipeForm, RatingForm, SearchForm, IngredientForm
from django.forms import formset_factory, inlineformset_factory


# Create your views here.

# Main page
def index(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Recipe.objects.filter(title__icontains=query)
    else:
        results = Recipe.objects.none()
    context = {'form': form, 'results': results}
    return render(request, 'recipe_app/index.html', context)

# Display all recipes
def recipes(request): # + sort type
    recipes = Recipe.objects.order_by('date_added') #sort by popularity?
    context = {'recipes':recipes}
    return render(request, 'recipe_app/all_recipes.html', context)

# Detailed recipe view
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    num_of_ratings = recipe.ratings.all().count()
    rating_sum = 0
    if num_of_ratings != 0:
        for rating in recipe.ratings.all():
            rating_sum += rating.score

        average = rating_sum / num_of_ratings
    else:
        average = 0

    ingredients = recipe.ingredients.all()
    ratings = recipe.ratings.all()
    instructions = recipe.instructions
    context = {'recipe':recipe, 
               'ingredients':ingredients, 
               'ratings':ratings, 
               'instructions': instructions,
               'average': average,
               'num_of_ratings':num_of_ratings}
    return render(request, 'recipe_app/recipe_detail.html', context)

# Handles the favorite button toggle
def toggle_favorite(request, recipe_id):
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user in recipe.favorited_by.all():
            recipe.favorited_by.remove(request.user)
        else:
            recipe.favorited_by.add(request.user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Add recipe view
def add_recipe(request):
    IngredientFormSet = formset_factory(IngredientForm, extra=7)
    if request.method != 'POST':
        recipe_form = RecipeForm()
        ingredient_formset = IngredientFormSet()
    else:
        recipe_form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(data=request.POST)
        print(recipe_form.is_valid())
        print(ingredient_formset.is_valid())
        if recipe_form.is_valid() and ingredient_formset.is_valid():
            new_recipe = recipe_form.save(commit=False)
            new_recipe.owner = request.user
            new_recipe.save()
            
            for ingredient in  ingredient_formset:
                if ingredient.has_changed():
                    ingredient = ingredient.save(commit=False)
                    ingredient.recipe = new_recipe
                    ingredient.save()

            return redirect('recipe_app:profile')
    context = {'form':recipe_form, 'ingform':ingredient_formset}
    return render(request,'recipe_app/add_recipe.html',context)

# Edit recipe view
def edit_recipe(request, recipe_id):
    
    recipe = get_object_or_404(Recipe, id=recipe_id)
    check_owner(recipe.owner, request.user)

    IngredientFormSet = inlineformset_factory(Recipe, Ingredients, form=IngredientForm, extra=7, can_delete=True)

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe)

        if recipe_form.is_valid() and ingredient_formset.is_valid():
            updated_recipe = recipe_form.save()
            ingredient_formset.save()
            return redirect('recipe_app:profile')
    else:
        recipe_form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe)

    context = {'form': recipe_form, 'ingform': ingredient_formset, 'recipe': recipe}
    return render(request, 'recipe_app/edit_recipe.html', context)

# Add rating view
def add_rating(request, recipe_id):

    recipe = Recipe.objects.get(id=recipe_id)

    if request.method != 'POST':
        form = RatingForm()
    else:
        form = RatingForm(data=request.POST)

        if form.is_valid():
            new_rating = form.save(commit=False)
            new_rating.recipe = recipe
            new_rating.owner = request.user
            new_rating.save()

            return redirect('recipe_app:recipe_detail', recipe_id=recipe_id)

    context = {'form': form, 'recipe': recipe}
    return render(request, 'recipe_app/add_rating.html', context)

# User profile
def profile(request):
    user = request.user
    favorites = user.favorites.all()
    form = RecipeForm()
    context = {'user': user, 'favorites': favorites}
    return render(request, 'recipe_app/profile.html')

# Add to favorites view


def testview(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'recipe_app/test.html', context)

def check_owner(owner, user):
    if owner != user:
        raise Http404