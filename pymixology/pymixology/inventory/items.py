from __future__ import annotations

from typing import Union


class Ingredient:
    """Basic ingredient tracking quantity with rough value support."""

    def __init__(self, name: str, quantity: float, expiry_date: str, value: float = 0.0) -> None:
        self.name = name
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.unit_value = (float(value) / quantity) if quantity else 0.0

    def info(self) -> str:
        value = self.current_value()
        value_part = f", Value: {value:.2f}" if value else ""
        return f"{self.name} ({self.quantity}) exp:{self.expiry_date}{value_part}"

    def __repr__(self) -> str:
        return f"Ingredient({self.info()})"

    def use(self, amount: Union[int, float]) -> bool:
        if not isinstance(amount, (int, float)):
            return False
        if amount <= 0 or amount > self.quantity:
            return False
        self.quantity -= amount
        return True

    def current_value(self) -> float:
        return self.unit_value * self.quantity


class Spirit(Ingredient):
    """Spirit placeholder; ABV support to be added later."""

    def __init__(self, name: str, quantity: float, expiry_date: str, abv: float = 0.0, value: float = 0.0) -> None:
        super().__init__(name, quantity, expiry_date, value=value)
        self.abv = abv

    def get_abv(self) -> float:
        return self.abv


class Mixer(Ingredient):
    """Mixer placeholder with carbonation flag."""

    def __init__(self, name: str, quantity: float, expiry_date: str, is_carbonated: bool, value: float = 0.0) -> None:
        super().__init__(name, quantity, expiry_date, value=value)
        self.is_carbonated = is_carbonated

    def is_fizzy(self) -> bool:
        return bool(self.is_carbonated)
