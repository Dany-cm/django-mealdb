import requests
from typing import Optional, Dict, List, Any


class MealDBService:
    BASE_URL = "https://www.themealdb.com/api/json/v1/1"

    @classmethod
    def _make_request(
        cls, endpoint: str, params: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(f"{cls.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    @classmethod
    def _get_meals_from_response(
        cls, endpoint: str, params: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        data = cls._make_request(endpoint, params)
        return data.get("meals") or [] if data else []

    @classmethod
    def search_meal_by_name(cls, name: str) -> List[Dict[str, Any]]:
        if not name or not name.strip():
            return []
        return cls._get_meals_from_response("search.php", {"s": name})

    @classmethod
    def get_meal_by_id(cls, meal_id: str) -> Optional[Dict[str, Any]]:
        if not meal_id:
            return None
        data = cls._make_request("lookup.php", {"i": meal_id})
        if data:
            meals = data.get("meals")
            return meals[0] if meals else None
        return None

    @classmethod
    def get_random_meal(cls) -> Optional[Dict[str, Any]]:
        data = cls._make_request("random.php")
        if data:
            meals = data.get("meals")
            return meals[0] if meals else None
        return None

    @classmethod
    def list_categories(cls) -> List[Dict[str, str]]:
        data = cls._make_request("categories.php")
        return data.get("categories") or [] if data else []

    @classmethod
    def list_areas(cls) -> List[Dict[str, Any]]:
        meals = cls._get_meals_from_response("list.php", {"a": "list"})
        return [{"strArea": meal["strArea"]} for meal in meals]

    @classmethod
    def list_ingredients(cls) -> List[Dict[str, Any]]:
        meals = cls._get_meals_from_response("list.php", {"i": "list"})
        return [{"strIngredient": meal["strIngredient"]} for meal in meals]

    @classmethod
    def filter_by_ingredient(cls, ingredient: str) -> List[Dict[str, Any]]:
        if not ingredient or not ingredient.strip():
            return []
        return cls._get_meals_from_response("filter.php", {"i": ingredient})

    @classmethod
    def filter_by_category(cls, category: str) -> List[Dict[str, Any]]:
        if not category or not category.strip():
            return []
        return cls._get_meals_from_response("filter.php", {"c": category})

    @classmethod
    def filter_by_area(cls, area: str) -> List[Dict[str, Any]]:
        if not area or not area.strip():
            return []
        return cls._get_meals_from_response("filter.php", {"a": area})

    @classmethod
    def get_meals_by_category(cls, category: str) -> List[Dict[str, Any]]:
        if not category or not category.strip():
            return []
        return cls._get_meals_from_response("filter.php", {"c": category})
