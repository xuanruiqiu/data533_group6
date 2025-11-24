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
    """Placeholder search that will be improved later."""
    return []


def filter_by_base(recipe_db: List[Dict[str, Any]], base_spirit: str) -> List[Dict[str, Any]]:
    """Return recipes that exactly match a base spirit (case sensitive for now)."""
    return [recipe for recipe in recipe_db if recipe.get("base") == base_spirit]


def display_recipe(cocktail_dict: Dict[str, Any]) -> None:
    """Print the name; formatted output will come later."""
    print("Recipe:", cocktail_dict.get("name", "Unknown"))
