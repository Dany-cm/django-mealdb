from typing import Any, Dict, List
from django import template

register = template.Library()


@register.filter
def get_ingredients(meal: Dict[str, Any]) -> List[Dict[str, str]]:
    ingredients: List[Dict[str, str]] = []
    # api returns in this format strIngredient1...20 same for strMeasure
    for i in range(1, 21):
        ingredient_key = f"strIngredient{i}"
        measure_key = f"strMeasure{i}"

        if ingredient_key in meal and meal[ingredient_key]:
            ingredient_name = str(meal[ingredient_key]).strip()
            measure = (
                str(meal.get(measure_key, "")).strip() if measure_key in meal else ""
            )

            if ingredient_name:
                ingredients.append(
                    {"name": ingredient_name, "measure": measure if measure else "—"}
                )

    return ingredients
