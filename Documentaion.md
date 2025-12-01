# PyMixology Project Documentation

## Project Overview
- Goal: A lightweight Python package that helps home users manage cocktail recipes, inventory, and personalized recommendations using JSON data.
- Data storage: `pymixology/data/cocktails.json` (50 sample recipes, editable, with per-ingredient amounts/units).
- Demo: `python main_test.py` runs an end-to-end example.

## Package Structure
```
pymixology/
├── recipes/
│   ├── catalog.py
│   └── tools.py
├── inventory/
│   ├── items.py
│   └── manager.py
├── recommendation/
│   ├── preference.py
│   └── suggester.py
├── data/
│   └── cocktails.json
└── __init__.py
```

## Module Details (Functions Only)
### recipes.catalog
- `load_recipes(filepath) -> list[dict]`: Load JSON recipes from disk and normalize ingredients to `{name, amount, unit}`.
- `search_cocktail(recipe_db, name) -> list[dict]`: Case-insensitive substring search on names.
- `filter_by_base(recipe_db, base_spirit) -> list[dict]`: Exact base match (case-insensitive).
- `display_recipe(cocktail_dict) -> None`: Prints name, formatted ingredient amounts, steps.

### recipes.tools
- `calculate_abv(ingredients) -> float`: Volume-weighted ABV using `vol` and `abv`.
- `estimate_cost(ingredients) -> float`: Per-drink cost using `price_per_bottle`, `bottle_vol`, `used_vol`.
- `unit_converter(amount, from_unit, to_unit) -> float`: Convert ml ↔ oz.
- `scale_recipe(cocktail_dict, servings) -> dict`: Deep-copies and scales ingredient `amount` fields.

### inventory.items (Inheritance)
- `Ingredient(name, quantity, expiry_date, value=0.0)`: Base class; tracks per-unit value, `info()`, `use(amount) -> bool`, and `current_value()`.
- `Spirit(name, quantity, expiry_date, abv, value=0.0)`: Extends Ingredient; adds `get_abv()`.
- `Mixer(name, quantity, expiry_date, is_carbonated, value=0.0)`: Extends Ingredient; adds `is_fizzy()`.

### inventory.manager
- `add_item(inventory_list, item_object) -> bool`: Append Ingredient subtype.
- `remove_item(inventory_list, item_name) -> bool`: Remove first matching name.
- `check_stock(inventory_list, item_name) -> float`: Return quantity or 0.
- `get_shopping_list(inventory_list, min_threshold) -> list[str]`: Names below threshold.
- `total_value(inventory_list) -> float`: Sum of remaining value for all items.

### recommendation.preference
- `set_flavor_profile(sweet, sour, bitter, strong) -> dict`: Save user taste profile.
- `record_review(reviews_db, cocktail_name, rating)`: Add or update rating (list or dict).
- `get_top_favorites(reviews_db, top_n=3) -> list[str]`: Top cocktails by rating.

### recommendation.suggester
- `get_makeable_cocktails(inventory_list, recipe_db) -> list[str]`: Recipes whose ingredients (names and required amounts when provided) are satisfied by inventory.
- `find_cocktails_with_ingredients(target_ingredients, recipe_db) -> list[str]`: Any overlap with target ingredients.
- `recommend_by_flavor(user_profile, recipe_db) -> list[str]`: Match recipe `flavor` to profile keys.
- `surprise_me(recipe_db) -> dict`: Random recipe choice.

## Data File (Mock)
- `pymixology/data/cocktails.json`: List of recipe dicts with fields `name`, `base`, `flavor`, `ingredients` (dicts containing `name`, `amount`, `unit`), `steps`. Feel free to edit or replace with your own recipes.

## Demonstration Script
- File: `main_test.py`
- Purpose: Simple walkthrough showing recipe search/filter, scaling, inventory operations, reviews, and recommendations.
- Run: `python main_test.py`

## How to Use in Your Own Code
```python
from pathlib import Path
from pymixology.recipes.catalog import load_recipes, search_cocktail
from pymixology.inventory.items import Spirit, Mixer
from pymixology.inventory.manager import add_item, get_shopping_list, total_value
from pymixology.recommendation.suggester import get_makeable_cocktails

recipes = load_recipes(Path("pymixology/data/cocktails.json"))
inventory = []
add_item(inventory, Spirit("Gin", 700, "2025-12-01", 0.40, value=35))
add_item(inventory, Mixer("Lime Juice", 200, "2024-12-31", False, value=3))

print(search_cocktail(recipes, "martini"))
print(get_makeable_cocktails(inventory, recipes))
print("Need to buy:", get_shopping_list(inventory, 500))
print("Inventory value:", round(total_value(inventory), 2))
```
