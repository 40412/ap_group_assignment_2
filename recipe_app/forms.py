from django import forms
from .models import Recipe,Rating, Ingredients

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title","instructions","portions","image"]
        labels = {"title":"Title","instructions":"Instructions","portions":"Portions","image":"Image"}

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["title","score","comment"]
        labels = {"title":"Otsikko","score":"Pisteet","comment":"Teksti"}

class SearchForm(forms.Form):
    query = forms.CharField()

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ['ingredient', 'amount', 'unit']