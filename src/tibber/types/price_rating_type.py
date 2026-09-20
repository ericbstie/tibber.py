from __future__ import annotations

"""A class representing the PriceRatingType type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING, List

from tibber.types.price_rating_entry import PriceRatingEntry

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class PriceRatingType:
    """A class to get the rating of a price in relative terms."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def min_energy(self) -> float:
        """Lowest Nordpool spot price over the time period"""
        return self.cache.get("minEnergy")

    @property
    def max_energy(self) -> float:
        """Highest Nordpool spot price over the time period"""
        return self.cache.get("maxEnergy")

    @property
    def min_total(self) -> float:
        """Lowest total price (incl. tax) over the time period"""
        return self.cache.get("minTotal")

    @property
    def max_total(self) -> float:
        """Highest total price (incl. tax) over the time period"""
        return self.cache.get("maxTotal")

    @property
    def currency(self) -> str:
        """The price currency"""
        return self.cache.get("currency")

    @property
    def entries(self) -> List[PriceRatingEntry]:
        """The individual price entries aggregated by hourly/daily/monthly values"""
        return [
            PriceRatingEntry(entry, self.tibber_client)
            for entry in self.cache.get("entries", [])
        ]
