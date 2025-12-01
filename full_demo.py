from pathlib import Path

from pymixology.recipes.catalog import load_recipes, search_cocktail, filter_by_base, display_recipe
from pymixology.recipes.tools import calculate_abv, estimate_cost, unit_converter, scale_recipe
from pymixology.inventory.items import Ingredient, Spirit, Mixer
from pymixology.inventory.manager import add_item, remove_item, check_stock, get_shopping_list, total_value
from pymixology.recommendation.preference import set_flavor_profile, record_review, get_top_favorites
from pymixology.recommendation.suggester import (
    get_makeable_cocktails,
    find_cocktails_with_ingredients,
    recommend_by_flavor,
    surprise_me,
)


def build_inventory() -> list[Ingredient]:
    """Create a sample inventory with spirits and mixers."""
    inventory: list[Ingredient] = []
    add_item(inventory, Spirit("Gin", 700, "2025-12-01", 0.40, value=35))
    add_item(inventory, Spirit("Dry Vermouth", 500, "2025-04-10", 0.18, value=15))
    add_item(inventory, Spirit("Tequila", 750, "2025-08-20", 0.45, value=40))
    add_item(inventory, Spirit("White Rum", 700, "2025-11-01", 0.40, value=32))
    add_item(inventory, Mixer("Triple Sec", 500, "2025-06-01", False, value=14))
    add_item(inventory, Mixer("Lime Juice", 300, "2024-12-31", False, value=4))
    add_item(inventory, Mixer("Sugar", 200, "2025-12-31", False, value=3))
    add_item(inventory, Mixer("Soda Water", 1000, "2025-05-05", True, value=6))
    add_item(inventory, Mixer("Mint", 50, "2024-08-01", False, value=2))
    add_item(inventory, Mixer("Salt", 100, "2026-01-01", False, value=1))
    return inventory


def main() -> None:
    data_path = Path(__file__).parent / "pymixology" / "data" / "cocktails.json"
    recipes = load_recipes(str(data_path))

    # Recipe queries
    print("\n== Recipe lookups ==")
    sunrise = search_cocktail(recipes, "sunrise")
    print("Search 'sunrise':", [r["name"] for r in sunrise])
    gin_based = filter_by_base(recipes, "Gin")
    print("Gin cocktails:", [r["name"] for r in gin_based[:5]], "...")
    print("Display first gin recipe:")
    display_recipe(gin_based[0])

    # Tools
    print("\n== Tools ==")
    abv = calculate_abv([{"vol": 45, "abv": 0.4}, {"vol": 15, "abv": 0.18}, {"vol": 30, "abv": 0.0}])
    print("Estimated ABV:", round(abv, 3))
    cost = estimate_cost(
        [
            {"price_per_bottle": 35, "bottle_vol": 700, "used_vol": 45},
            {"price_per_bottle": 20, "bottle_vol": 750, "used_vol": 15},
        ]
    )
    print("Estimated cost per drink:", round(cost, 2))
    print("50 ml to oz:", round(unit_converter(50, "ml", "oz"), 2))
    scaled = scale_recipe(
        {
            "name": "Mini Sour",
            "servings": 1,
            "ingredients": [
                {"name": "Whiskey", "amount": 50, "unit": "ml"},
                {"name": "Lemon Juice", "amount": 20, "unit": "ml"},
                {"name": "Simple Syrup", "amount": 15, "unit": "ml"},
            ],
        },
        servings=3,
    )
    print("Scaled ingredients (serves 3):", scaled["ingredients"])

    # Inventory: creation, info, use, stock checks
    print("\n== Inventory ==")
    inventory = build_inventory()
    gin = inventory[0]
    print("Info:", gin.info(), "ABV:", gin.get_abv())
    fizzy = inventory[7]
    print("Soda is fizzy?:", fizzy.is_fizzy())
    print("Use 60ml gin:", gin.use(60), "remaining:", gin.quantity)
    print("Stock for Salt:", check_stock(inventory, "Salt"))
    print("Remove Mint:", remove_item(inventory, "Mint"))
    print("Shopping list (below 150):", get_shopping_list(inventory, 150))
    print("Inventory value ($ est.):", round(total_value(inventory), 2))

    # Recommendations: profile, reviews, matching
    print("\n== Recommendations ==")
    profile = set_flavor_profile(sweet=4, sour=7, bitter=6, strong=8)
    print("Flavor profile:", profile)
    reviews = {}
    record_review(reviews, "Martini", 5)
    record_review(reviews, "Mojito", 4)
    record_review(reviews, "Old Fashioned", 5)
    print("Top favorites:", get_top_favorites(reviews, top_n=3))
    makeable = get_makeable_cocktails(inventory, recipes)
    print("Makeable now:", makeable[:5], "...")
    ginger_matches = find_cocktails_with_ingredients(["Ginger Beer"], recipes)
    print("With Ginger Beer:", ginger_matches[:5], "...")
    flavor_recos = recommend_by_flavor(profile, recipes)
    print("By flavor profile:", flavor_recos[:5], "...")
    surprise = surprise_me(recipes)
    print("Surprise pick:", surprise.get("name"))


if __name__ == "__main__":
    main()
