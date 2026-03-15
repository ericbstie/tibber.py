from __future__ import annotations

"""A class representing the HomeConsumptionPageInfo type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class HomeConsumptionPageInfo:
    """A class containing household electricity consumption information for a time period."""

    def __init__(self, resolution: str, data: dict, tibber_client: "Account"):
        self.resolution = resolution
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def end_cursor(self) -> str:
        """The global ID of the last element in the list"""
        return self.cache.get("endCursor")

    @property
    def has_next_page(self) -> bool:
        """True if further pages are available"""
        return self.cache.get("hasNextPage")

    @property
    def has_previous_page(self) -> bool:
        """True if previous pages are available"""
        return self.cache.get("hasPreviousPage")

    @property
    def start_cursor(self) -> str:
        """The global ID of the first element in the list"""
        return self.cache.get("startCursor")

    @property
    def count(self) -> int:
        """The number of elements in the list"""
        return self.cache.get("count")

    @property
    def currency(self) -> str:
        """The currency of the page"""
        return self.cache.get("currency")

    @property
    def total_cost(self) -> float:
        """Page total cost"""
        return self.cache.get("totalCost")

    @property
    def total_consumption(self) -> float:
        """Total consumption for page"""
        return self.cache.get("totalConsumption")

    @property
    def filtered(self) -> int:
        """Number of entries that have been filtered from result set due to empty nodes"""
        return self.cache.get("filtered")
