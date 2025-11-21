from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.views.decorators.http import require_http_methods
from recipe.services import MealDBService


def index(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {
        "categories": MealDBService.list_categories(),
        "areas": MealDBService.list_areas(),
        "ingredients": MealDBService.list_ingredients(),
    }
    return render(request, "recipe/index.html", context)


@require_http_methods(["GET"])
def search_meals(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    meals = MealDBService.search_meal_by_name(query) if query else []
    return render(request, "recipe/partials/meal_grid.html", {"meals": meals})


@require_http_methods(["GET"])
def random_meal(request: HttpRequest) -> HttpResponse:
    meal = MealDBService.get_random_meal()
    if meal:
        return render(request, "recipe/partials/meal_detail.html", {"meal": meal})
    return HttpResponse('<p class="text-center text-red-500">No meal found</p>')


@require_http_methods(["GET"])
def meal_detail(request: HttpRequest, meal_id: str) -> HttpResponse:
    meal = MealDBService.get_meal_by_id(meal_id)
    if meal:
        return render(request, "recipe/partials/meal_detail.html", {"meal": meal})
    return HttpResponse('<p class="text-center text-red-500">Meal not found</p>')


@require_http_methods(["GET"])
def filter_meals(request: HttpRequest) -> HttpResponse:
    filter_type = request.GET.get("type", "").strip()
    filter_value = request.GET.get("value", "").strip()

    meals = []

    match filter_type:
        case "category":
            if filter_value:
                meals = MealDBService.filter_by_category(filter_value)
        case "area":
            if filter_value:
                meals = MealDBService.filter_by_area(filter_value)
        case "ingredient":
            if filter_value:
                meals = MealDBService.filter_by_ingredient(filter_value)
        case _:
            pass

    return render(request, "recipe/partials/meal_grid.html", {"meals": meals})


@require_http_methods(["GET"])
def list_categories(request: HttpRequest) -> HttpResponse:
    categories = MealDBService.list_categories()
    return render(
        request, "recipe/partials/categories_list.html", {"categories": categories}
    )


@require_http_methods(["GET"])
def category_meals(request: HttpRequest, category_name: str) -> HttpResponse:
    meals = MealDBService.filter_by_category(category_name)
    return render(
        request,
        "recipe/partials/meal_grid.html",
        {"meals": meals, "category": category_name},
    )
