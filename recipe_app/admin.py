from django.contrib import admin
from .models import Recipe
from .models import Ingredients

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredients)