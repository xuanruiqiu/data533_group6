from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any


def load_recipes(filepath: str) -> List[Dict[str, Any]]:
    """Load recipes from JSON if file exists; otherwise return an empty list."""
    path = Path(filepath)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def search_cocktail(recipe_db: List[Dict[str, Any]], name: str) -> List[Dict[str, Any]]:
    """Case-insensitive substring search across cocktail names."""
    query = name.lower().strip()
    return [recipe for recipe in recipe_db if query in str(recipe.get("name", "")).lower()]


def filter_by_base(recipe_db: List[Dict[str, Any]], base_spirit: str) -> List[Dict[str, Any]]:
    """Return recipes that exactly match a base spirit (case-insensitive)."""
    target = base_spirit.lower().strip()
    return [recipe for recipe in recipe_db if str(recipe.get("base", "")).lower() == target]


def display_recipe(cocktail_dict: Dict[str, Any]) -> None:
    """Print a simple recipe summary."""
    name = cocktail_dict.get("name", "Unknown")
    ingredients = cocktail_dict.get("ingredients", [])
    steps = cocktail_dict.get("steps", [])
    print(f"Recipe: {name}")
    if ingredients:
        print("Ingredients:")
        for item in ingredients:
            print("-", item)
    if steps:
        print("Steps:")
        for i, step in enumerate(steps, start=1):
            print(f\"{i}. {step}\")
