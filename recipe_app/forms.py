from django import forms
from .models import Recipe,Rating

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title","instructions","portions","image"]
        labels = {"title":"Title","instructions":"Instructions","portions":"Portions","image":"Image"}

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["title","score","comment"]
        labels = {"title":"Title","score":"Score","comment":"Comment"}