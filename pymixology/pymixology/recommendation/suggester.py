from __future__ import annotations

import random
from typing import Iterable, List, Dict, Any

from pymixology.inventory.items import Ingredient


def get_makeable_cocktails(inventory_list: List[Ingredient], recipe_db: Iterable[Dict[str, Any]]) -> List[str]:
    """Recommend cocktails whose ingredient names are present in inventory (quantity ignored)."""
    inventory_names = {item.name.lower() for item in inventory_list}
    ready = []
    for recipe in recipe_db:
        ingredients = {str(item.get("name", "")).lower() for item in recipe.get("ingredients", []) if isinstance(item, dict)}
        if ingredients and ingredients.issubset(inventory_names):
            ready.append(recipe.get("name", ""))
    return ready


def find_cocktails_with_ingredients(target_ingredients: List[str], recipe_db: Iterable[Dict[str, Any]]) -> List[str]:
    """Cocktails that include any of the target ingredients."""
    targets = {item.lower() for item in target_ingredients}
    matches = []
    for recipe in recipe_db:
        ingredients = {str(item.get("name", "")).lower() for item in recipe.get("ingredients", []) if isinstance(item, dict)}
        if ingredients & targets:
            matches.append(recipe.get("name", ""))
    return matches


def recommend_by_flavor(user_profile: Dict[str, int], recipe_db: Iterable[Dict[str, Any]]) -> List[str]:
    """Match simple flavor tags to a stored profile."""
    ranked = []
    for recipe in recipe_db:
        key = str(recipe.get("flavor", "")).lower()
        score = user_profile.get(key, 0)
        if score > 0:
            ranked.append((score, recipe.get("name", "")))
    ranked.sort(reverse=True, key=lambda item: item[0])
    return [name for _score, name in ranked]


def surprise_me(recipe_db: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    recipes = list(recipe_db)
    return random.choice(recipes) if recipes else {}
