from __future__ import annotations

from typing import List

from .items import Ingredient


def add_item(inventory_list: List[Ingredient], item_object: Ingredient) -> bool:
    inventory_list.append(item_object)
    return True


def remove_item(inventory_list: List[Ingredient], item_name: str) -> bool:
    target = item_name.lower().strip()
    for idx, item in enumerate(inventory_list):
        if item.name.lower() == target:
            del inventory_list[idx]
            return True
    return False


def check_stock(inventory_list: List[Ingredient], item_name: str) -> float:
    target = item_name.lower().strip()
    for item in inventory_list:
        if item.name.lower() == target:
            return item.quantity
    return 0.0


def get_shopping_list(inventory_list: List[Ingredient], min_threshold: float) -> List[str]:
    return []


def total_value(inventory_list: List[Ingredient]) -> float:
    return 0.0
