from __future__ import annotations

import copy
from typing import List, Dict, Any

_OZ_TO_ML = 29.5735


def calculate_abv(ingredients: List[Dict[str, float]]) -> float:
    """Volume-weighted ABV estimate."""
    total_volume = sum(max(0, item.get("vol", 0)) for item in ingredients)
    if total_volume <= 0:
        return 0.0
    weighted_abv = sum(max(0, item.get("vol", 0)) * item.get("abv", 0) for item in ingredients)
    return weighted_abv / total_volume


def estimate_cost(ingredients: List[Dict[str, float]]) -> float:
    """Estimate cost using bottle price and usage."""
    cost = 0.0
    for item in ingredients:
        bottle_vol = item.get("bottle_vol", 0) or 1
        if bottle_vol <= 0:
            raise ValueError("Bottle volume must be greater than zero.")
        price_per_bottle = item.get("price_per_bottle", 0)
        used_vol = item.get("used_vol", 0)
        if used_vol < 0:
            raise ValueError("Used volume must be non-negative.")
        cost += (price_per_bottle / bottle_vol) * used_vol
    return cost


def unit_converter(amount: float, from_unit: str, to_unit: str) -> float:
    """Convert ml<->oz with a coarse factor."""
    f_unit = from_unit.lower()
    t_unit = to_unit.lower()
    if f_unit == t_unit:
        return amount
    if f_unit == "ml" and t_unit == "oz":
        return amount / _OZ_TO_ML
    if f_unit == "oz" and t_unit == "ml":
        return amount * _OZ_TO_ML
    raise ValueError("Unsupported unit conversion.")


def scale_recipe(cocktail_dict: Dict[str, Any], servings: int) -> Dict[str, Any]:
    """Scale each numeric ingredient amount by the servings factor."""
    if servings <= 0:
        raise ValueError("Servings must be positive.")
    factor = servings / (cocktail_dict.get("servings", 1) or 1)
    new_recipe = copy.deepcopy(cocktail_dict)
    scaled = []
    for ingredient in new_recipe.get("ingredients", []):
        if isinstance(ingredient, dict) and "amount" in ingredient:
            amount = ingredient.get("amount")
            if isinstance(amount, (int, float)):
                ingredient["amount"] = amount * factor
        scaled.append(ingredient)
    new_recipe["ingredients"] = scaled
    new_recipe["servings"] = servings
    return new_recipe
