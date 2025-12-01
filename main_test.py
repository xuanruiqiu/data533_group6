from pathlib import Path

from pymixology.inventory.items import Mixer, Spirit
from pymixology.inventory.manager import add_item, remove_item, check_stock, get_shopping_list, total_value
from pymixology.recipes.catalog import load_recipes, search_cocktail, filter_by_base, display_recipe
from pymixology.recipes.tools import calculate_abv, estimate_cost, unit_converter, scale_recipe
from pymixology.recommendation.preference import set_flavor_profile, record_review, get_top_favorites
from pymixology.recommendation.suggester import (
    get_makeable_cocktails,
    find_cocktails_with_ingredients,
    recommend_by_flavor,
    surprise_me,
)


def main() -> None:
    data_path = Path(__file__).parent / "pymixology" / "data" / "cocktails.json"
    recipes = load_recipes(str(data_path))

    inventory = []
    add_item(inventory, Spirit("Gin", 700, "2025-12-01", 0.40, value=35))
    add_item(inventory, Spirit("Dry Vermouth", 500, "2025-04-10", 0.18, value=15))
    add_item(inventory, Mixer("Lime Juice", 200, "2024-12-31", False, value=3))
    add_item(inventory, Mixer("Simple Syrup", 150, "2024-12-31", False, value=2))

    print("Search for 'mart':", [item.get("name") for item in search_cocktail(recipes, "mart")])
    print("Filter by base Gin:", [item.get("name") for item in filter_by_base(recipes, "Gin")])

    print("Martini recipe:")
    display_recipe(search_cocktail(recipes, "martini")[0])

    abv_estimate = calculate_abv(
        [
            {"vol": 60, "abv": 0.4},
            {"vol": 10, "abv": 0.18},
            {"vol": 30, "abv": 0.0},
        ]
    )
    print("Estimated ABV:", round(abv_estimate, 3))

    cost_estimate = estimate_cost(
        [
            {"price_per_bottle": 35, "bottle_vol": 700, "used_vol": 60},
            {"price_per_bottle": 20, "bottle_vol": 750, "used_vol": 10},
        ]
    )
    print("Estimated cost per drink:", round(cost_estimate, 2))

    print("30 ml to oz:", round(unit_converter(30, "ml", "oz"), 2))

    scaled = scale_recipe(
        {
            "name": "Sample Sour",
            "servings": 1,
            "ingredients": [
                {"name": "Whiskey", "amount": 60, "unit": "ml"},
                {"name": "Lemon Juice", "amount": 25, "unit": "ml"},
            ],
        },
        servings=2,
    )
    print("Scaled sour amounts:", scaled["ingredients"])

    print("Inventory check for Gin:", check_stock(inventory, "Gin"))
    print("Remove Lime Juice:", remove_item(inventory, "Lime Juice"))
    print("Shopping list below 200ml:", get_shopping_list(inventory, 200))
    print("Total inventory value ($ est.):", round(total_value(inventory), 2))

    profile = set_flavor_profile(sweet=3, sour=8, bitter=2, strong=7)
    print("Recommendations by flavor:", recommend_by_flavor(profile, recipes))

    reviews = {}
    record_review(reviews, "Martini", 5)
    record_review(reviews, "Mojito", 4)
    print("Top favorites:", get_top_favorites(reviews, top_n=2))

    print("Can make now:", get_makeable_cocktails(inventory, recipes))
    print("Find cocktails with Lemon Juice:", find_cocktails_with_ingredients(["Lemon Juice"], recipes))

    print("Random pick:", surprise_me(recipes).get("name"))


if __name__ == "__main__":
    main()
