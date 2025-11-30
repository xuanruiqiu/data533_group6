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
    if not isinstance(data, list):
        raise ValueError("Recipe data must be a list of dicts.")
    return [_normalize_recipe(recipe) for recipe in data]


def search_cocktail(recipe_db: List[Dict[str, Any]], name: str) -> List[Dict[str, Any]]:
    """Case-insensitive substring search across cocktail names."""
    query = name.lower().strip()
    if not query:
        return []
    return [recipe for recipe in recipe_db if query in str(recipe.get("name", "")).lower()]


def filter_by_base(recipe_db: List[Dict[str, Any]], base_spirit: str) -> List[Dict[str, Any]]:
    """Return recipes that exactly match a base spirit (case-insensitive)."""
    target = base_spirit.lower().strip()
    return [recipe for recipe in recipe_db if str(recipe.get("base", "")).lower() == target]


def display_recipe(cocktail_dict: Dict[str, Any]) -> None:
    """Print a simple recipe summary."""
    name = cocktail_dict.get("name", "Unknown")
    ingredients = [_normalize_ingredient(item) for item in cocktail_dict.get("ingredients", [])]
    steps = cocktail_dict.get("steps", [])
    print(f"Recipe: {name}")
    if ingredients:
        print("Ingredients:")
        for item in ingredients:
            print("-", _format_ingredient(item))
    if steps:
        print("Steps:")
        for i, step in enumerate(steps, start=1):
            print(f"{i}. {step}")


def _normalize_ingredient(ingredient: Any) -> Dict[str, Any]:
    """Ensure each ingredient is a dict with consistent keys."""
    if isinstance(ingredient, dict):
        return {
            "name": ingredient.get("name", ""),
            "amount": ingredient.get("amount"),
            "unit": ingredient.get("unit"),
        }
    return {"name": ingredient, "amount": None, "unit": None}


def _normalize_recipe(recipe: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize ingredient entries inside a recipe dict."""
    normalized = dict(recipe)
    normalized["ingredients"] = [_normalize_ingredient(item) for item in recipe.get("ingredients", [])]
    return normalized


def _format_ingredient(ingredient: Dict[str, Any]) -> str:
    """Render an ingredient dict into a friendly string."""
    name = ingredient.get("name", "Unknown ingredient")
    amount = ingredient.get("amount")
    unit = ingredient.get("unit")
    if amount is None:
        return name
    if isinstance(amount, (int, float)):
        amount_str = f"{amount:.2f}".rstrip("0").rstrip(".")
    else:
        amount_str = str(amount)
    if unit:
        return f"{amount_str} {unit} {name}"
    return f"{amount_str} {name}"
