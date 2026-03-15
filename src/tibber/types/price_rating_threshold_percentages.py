from __future__ import annotations

"""A class representing the PriceRatingThresholdPercentages type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class PriceRatingThresholdPercentages:
    """A class to get price info."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def high(self) -> float:
        """The percentage difference when the price is considered to be 'high' (market dependent)"""
        return self.cache.get("high")

    @property
    def low(self) -> float:
        """The percentage difference when the price is considered to be 'low' (market dependent)"""
        return self.cache.get("current")
