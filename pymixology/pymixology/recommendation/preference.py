from __future__ import annotations

from typing import Dict, Any

user_profile: Dict[str, int] = {}


def set_flavor_profile(sweet: int, sour: int, bitter: int, strong: int) -> Dict[str, int]:
    global user_profile
    user_profile = {
        "sweet": int(sweet),
        "sour": int(sour),
        "bitter": int(bitter),
        "strong": int(strong),
    }
    return user_profile


def record_review(reviews_db: Any, cocktail_name: str, rating: int):
    if isinstance(reviews_db, dict):
        reviews_db[cocktail_name] = int(rating)
    elif isinstance(reviews_db, list):
        reviews_db.append({"cocktail": cocktail_name, "rating": int(rating)})
    return reviews_db


def get_top_favorites(reviews_db: Any, top_n: int = 3):
    """Return top-rated cocktail names."""
    if top_n <= 0:
        return []
    pairs = []
    if isinstance(reviews_db, dict):
        pairs = list(reviews_db.items())
    elif isinstance(reviews_db, list):
        pairs = [(item.get("cocktail"), item.get("rating", 0)) for item in reviews_db]
    else:
        raise TypeError("reviews_db must be a list or dict.")

    sorted_pairs = sorted(pairs, key=lambda item: item[1], reverse=True)
    return [name for name, _rating in sorted_pairs[:top_n] if name]
