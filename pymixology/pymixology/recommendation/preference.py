from __future__ import annotations

from typing import Dict, Any

user_profile: Dict[str, int] = {}


def set_flavor_profile(sweet: int, sour: int, bitter: int, strong: int) -> Dict[str, int]:
    global user_profile
    user_profile = {
        "sweet": sweet,
        "sour": sour,
        "bitter": bitter,
        "strong": strong,
    }
    return user_profile


def record_review(reviews_db: Any, cocktail_name: str, rating: int):
    if isinstance(reviews_db, dict):
        reviews_db[cocktail_name] = rating
    elif isinstance(reviews_db, list):
        reviews_db.append({"cocktail": cocktail_name, "rating": rating})
    return reviews_db


def get_top_favorites(reviews_db: Any, top_n: int = 3):
    return []
