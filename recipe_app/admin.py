from django.contrib import admin
from .models import Recipe, Ingredients, Rating

# Register your models here.

admin.site.register([Recipe, Ingredients, Rating])