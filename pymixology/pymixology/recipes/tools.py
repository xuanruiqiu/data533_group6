from __future__ import annotations

from typing import List, Dict, Any


def calculate_abv(ingredients: List[Dict[str, float]]) -> float:
    """Volume-weighted ABV estimate."""
    total_volume = sum(item.get("vol", 0) for item in ingredients)
    if total_volume <= 0:
        return 0.0
    weighted_abv = sum(item.get("vol", 0) * item.get("abv", 0) for item in ingredients)
    return weighted_abv / total_volume


def estimate_cost(ingredients: List[Dict[str, float]]) -> float:
    """Estimate cost using bottle price and usage."""
    cost = 0.0
    for item in ingredients:
        bottle_vol = item.get("bottle_vol", 0) or 1
        price_per_bottle = item.get("price_per_bottle", 0)
        used_vol = item.get("used_vol", 0)
        cost += (price_per_bottle / bottle_vol) * used_vol
    return cost


def unit_converter(amount: float, from_unit: str, to_unit: str) -> float:
    """Convert ml<->oz with a coarse factor."""
    if from_unit == to_unit:
        return amount
    if from_unit == "ml" and to_unit == "oz":
        return amount / 30
    if from_unit == "oz" and to_unit == "ml":
        return amount * 30
    return amount


def scale_recipe(cocktail_dict: Dict[str, Any], servings: int) -> Dict[str, Any]:
    """Scale each numeric ingredient amount by the servings factor."""
    if servings <= 0:
        return cocktail_dict
    factor = servings / (cocktail_dict.get("servings", 1) or 1)
    new_recipe = dict(cocktail_dict)
    scaled = []
    for ingredient in cocktail_dict.get("ingredients", []):
        if isinstance(ingredient, dict) and "amount" in ingredient:
            entry = ingredient.copy()
            amount = entry.get("amount")
            if isinstance(amount, (int, float)):
                entry["amount"] = amount * factor
            scaled.append(entry)
        else:
            scaled.append(ingredient)
    new_recipe["ingredients"] = scaled
    new_recipe["servings"] = servings
    return new_recipe
