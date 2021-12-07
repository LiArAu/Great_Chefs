
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('recipe_detail/<int:pk>', views.RecipeDetailView.as_view(), name = 'recipe_detail'),
    path('category_detail/<int:pk>', views.CatDetailView.as_view(), name = 'category_detail'),
    path('sharenozone/', views.nozone, name = 'nozone'),
    path('sharezone/', views.havezone, name = 'havezone'),
    path('add', views.add_recipe, name = 'add')
]
