from __future__ import annotations

"""A class representing the SubscriptionPriceConnectionPageInfo type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tibber.account import Account


class SubscriptionPriceConnectionPageInfo:
    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def end_cursor(self) -> str:
        return self.cache.get("endCursor")

    @property
    def has_next_page(self) -> bool:
        return self.cache.get("hasNextPage")

    @property
    def has_previous_page(self) -> bool:
        return self.cache.get("hasPreviousPage")

    @property
    def start_cursor(self) -> str:
        return self.cache.get("startCursor")

    @property
    def resolution(self) -> str:
        return self.cache.get("resolution")

    @property
    def currency(self) -> str:
        return self.cache.get("currency")

    @property
    def count(self) -> int:
        return self.cache.get("count")

    @property
    def precision(self) -> int:
        return self.cache.get("precision")

    @property
    def min_energy(self) -> float:
        return self.cache.get("minEnergy")

    @property
    def min_total(self) -> float:
        return self.cache.get("minTotal")

    @property
    def max_energy(self) -> float:
        return self.cache.get("maxEnergy")

    @property
    def max_total(self) -> float:
        return self.cache.get("maxTotal")
