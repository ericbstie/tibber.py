from __future__ import annotations

"""A class representing the PriceRatingEntry type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class PriceRatingEntry:
    """A class to get the rating of a price in relative terms."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def time(self) -> str:
        """The start time of the price"""
        return self.cache.get("time")

    @property
    def energy(self) -> float:
        """Nordpool spot price"""
        return self.cache.get("energy")

    @property
    def total(self) -> float:
        """The total price (incl. tax)"""
        return self.cache.get("total")

    @property
    def tax(self) -> float:
        """The tax part of the price (guarantee of origin certificate, energy tax (Sweden only) and VAT)"""
        return self.cache.get("tax")

    @property
    def difference(self) -> float:
        """The percentage difference compared to the trailing price average (1 day for 'hourly', 30 days for 'daily' and 32 months for 'monthly')"""
        return self.cache.get("difference")

    @property
    def level(self) -> str:
        """The price level compared to recent price values (calculated using 'difference' and 'priceRating.thresholdPercentages')"""
        return self.cache.get("level")
