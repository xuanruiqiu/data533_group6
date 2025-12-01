# `pymixology` Package Function Details

This document provides a detailed explanation of the functions and classes available in the `pymixology` package found in `data533_group6`. The package is designed to manage a cocktail bar's inventory, recipe catalog, and recommendations.

## Directory Structure

```
pymixology/
├── inventory/
│   ├── items.py       # Classes for inventory items (Ingredients)
│   └── manager.py     # Functions to manage the inventory list
├── recipes/
│   ├── catalog.py     # Functions to load and query recipes
│   └── tools.py       # Utility functions for recipe calculations
└── recommendation/
    ├── preference.py  # Functions for user preferences and reviews
    └── suggester.py   # Functions for cocktail recommendations
```

---

## 1. Inventory Management (`pymixology.inventory`)

### `items.py` - Ingredient Classes

This module defines the classes used to represent items in the inventory.

*   **`Ingredient` Class**:
    *   **`__init__(name, quantity, expiry_date, value)`**: Initializes an ingredient with a name, quantity (e.g., ml), expiry date, and total value. Calculates `unit_value` automatically.
    *   **`info()`**: Returns a string summary of the item (Name, Quantity, Value).
    *   **`use(amount)`**: Reduces the item's quantity by `amount` if sufficient stock exists. Returns `True` on success, `False` otherwise.
    *   **`current_value()`**: Calculates the total value based on the current quantity and unit value.

*   **`Spirit` Class (Inherits from `Ingredient`)**:
    *   **`__init__(..., abv, ...)`**: Adds an `abv` (Alcohol by Volume) attribute to the standard ingredient.
    *   **`get_abv()`**: Returns the ABV of the spirit.

*   **`Mixer` Class (Inherits from `Ingredient`)**:
    *   **`__init__(..., is_carbonated, ...)`**: Adds an `is_carbonated` boolean attribute.
    *   **`is_fizzy()`**: Returns `True` if the mixer is carbonated.

### `manager.py` - Inventory Utilities

Functions to manipulate lists of `Ingredient` objects.

*   **`add_item(inventory_list, item_object)`**: Appends a new `Ingredient` (or subclass) object to the provided list. Raises `TypeError` if the object is invalid.
*   **`remove_item(inventory_list, item_name)`**: Removes the first item matching `item_name` (case-insensitive) from the list. Returns `True` if found and removed.
*   **`check_stock(inventory_list, item_name)`**: Returns the current quantity of a specific item. Returns `0.0` if not found.
*   **`get_shopping_list(inventory_list, min_threshold)`**: Returns a list of names for items whose quantity is below `min_threshold`.
*   **`total_value(inventory_list)`**: Sums the `current_value()` of all items in the inventory list.

---

## 2. Recipe Management (`pymixology.recipes`)

### `catalog.py` - Recipe Loading & Querying

*   **`load_recipes(filepath)`**: Reads a JSON file containing cocktail recipes and returns a list of dictionaries. Normalizes ingredient formats.
*   **`search_cocktail(recipe_db, name)`**: Returns a list of recipes where the cocktail name partially matches the query string (case-insensitive).
*   **`filter_by_base(recipe_db, base_spirit)`**: Returns recipes that match the specified `base_spirit` exactly (case-insensitive).
*   **`display_recipe(cocktail_dict)`**: Prints a formatted view of the recipe, including its name, ingredients list, and step-by-step instructions.

### `tools.py` - Recipe Calculations

*   **`calculate_abv(ingredients)`**: Estimates the final ABV of a drink based on a list of ingredients with volumes and ABVs. Uses a volume-weighted average.
*   **`estimate_cost(ingredients)`**: Calculates the cost of a single drink. Requires ingredients to have `price_per_bottle`, `bottle_vol`, and `used_vol`.
*   **`unit_converter(amount, from_unit, to_unit)`**: Converts volumes between "ml" and "oz".
*   **`scale_recipe(cocktail_dict, servings)`**: Returns a new recipe dictionary with ingredient amounts multiplied to match the requested number of `servings`.

---

## 3. Recommendations (`pymixology.recommendation`)

### `preference.py` - User Preferences

*   **`set_flavor_profile(sweet, sour, bitter, strong)`**: Stores and returns a dictionary representing the user's flavor preferences (0-10 scale).
*   **`record_review(reviews_db, cocktail_name, rating)`**: Adds or updates a rating for a cocktail in the provided database (supports both list and dict storage).
*   **`get_top_favorites(reviews_db, top_n)`**: Returns the names of the top `top_n` rated cocktails, sorted by rating descending.

### `suggester.py` - Recommendation Logic

*   **`get_makeable_cocktails(inventory_list, recipe_db)`**: Checks the inventory against all recipes. Returns a list of cocktail names where the inventory contains sufficient quantity of all required ingredients.
*   **`find_cocktails_with_ingredients(target_ingredients, recipe_db)`**: Returns cocktail names that contain *any* of the specified `target_ingredients`.
*   **`recommend_by_flavor(user_profile, recipe_db)`**: Scores recipes based on the user's flavor profile. Matches the recipe's "flavor" tag to the user's preference score for that flavor.
*   **`surprise_me(recipe_db)`**: Returns a random cocktail recipe from the database.

---

## Usage Examples

See `full_demo.py` for a comprehensive script demonstrating how these modules work together to:
1.  Build an inventory.
2.  Search and display recipes.
3.  Calculate costs and scaling.
4.  Generate recommendations based on inventory and taste.

