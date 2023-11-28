# Recipe app urls
from django.urls import path
from . import views
app_name = 'recipe_app'
urlpatterns = [
    # Main page, using same naming as in the book
    path('', views.index, name='index')
]