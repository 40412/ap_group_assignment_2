from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.

class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='recipes')
    title = models.CharField(max_length=100)
    instructions = models.TextField()
    portions = models.IntegerField()
    image = models.ImageField(upload_to='pics', null=True)
    favorited_by = models.ManyToManyField(User, related_name='favorites', blank=True)
    date_added = models.DateTimeField(auto_now_add=True, editable=False, null=True) #date_added and date_modified are read-only
    date_modified = models.DateTimeField(auto_now=True, editable=False) #and handled by the system
                                          
    
class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING, related_name='ingredients')
    ingredient = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=7, decimal_places=1)
    unit = models.CharField(max_length=10)

    def __str__(self):
        """Returns a string representation of the model"""
        return f"{self.ingredient} {self.amount} {self.unit}"

class Favorites(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')

class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='ratings')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    title = models.CharField(max_length=100)
    score = models.IntegerField(validators=[MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    date_modified = models.DateTimeField(auto_now=True, editable=False)