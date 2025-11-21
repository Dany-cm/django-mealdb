from django.urls import path
from recipe import views

app_name = "recipe"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_meals, name="search"),
    path("random/", views.random_meal, name="random"),
    path("meal/<str:meal_id>/", views.meal_detail, name="meal_detail"),
    path("filter/", views.filter_meals, name="filter"),
    path("categories/", views.list_categories, name="categories"),
    path("category/<str:category_name>/", views.category_meals, name="category_meals"),
]
