from __future__ import annotations

import random
from typing import Iterable, List, Dict, Any

from pymixology.inventory.items import Ingredient


def get_makeable_cocktails(inventory_list: List[Ingredient], recipe_db: Iterable[Dict[str, Any]]) -> List[str]:
    return []


def find_cocktails_with_ingredients(target_ingredients: List[str], recipe_db: Iterable[Dict[str, Any]]) -> List[str]:
    return []


def recommend_by_flavor(user_profile: Dict[str, int], recipe_db: Iterable[Dict[str, Any]]) -> List[str]:
    return []


def surprise_me(recipe_db: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    recipes = list(recipe_db)
    return random.choice(recipes) if recipes else {}
