from __future__ import annotations

"""A class representing the Price type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class Price:
    """A class to get price info."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def total(self) -> float:
        """The total price (energy + taxes)"""
        return self.cache.get("total")

    @property
    def energy(self) -> float:
        """Nordpool spot price"""
        return self.cache.get("energy")

    @property
    def tax(self) -> float:
        """The tax part of the price (guarantee of origin certificate, energy tax (Sweden only) and VAT)"""
        return self.cache.get("tax")

    @property
    def starts_at(self) -> str:
        """The start time of the price"""
        return self.cache.get("startsAt")

    @property
    def currency(self) -> str:
        """The price currency"""
        return self.cache.get("currency")

    @property
    def level(self) -> str:
        """The price level compared to recent price values"""
        return self.cache.get("level")
