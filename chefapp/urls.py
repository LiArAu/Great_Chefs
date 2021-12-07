from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('recipe_detail/<int:pk>', views.RecipeDetailView.as_view(), name = 'recipe_detail'),
    path('category_detail/<int:pk>', views.CatDetailView.as_view(), name = 'category_detail'),
    path('profile_detail/<str:pk>', views.ProfDetailView.as_view(), name = 'profile_detail'),
    path('noperm',views.no_perm, name="view_no_perm"),
    path('yourzone', views.zone, name='view_zone'),
    path('add', views.add_recipe, name = 'add')
]
