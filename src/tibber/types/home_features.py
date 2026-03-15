from __future__ import annotations

"""A class representing the HomeFeatures type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class HomeFeatures:
    """A class to get information about the features of a TibberHome."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: Account = tibber_client

    @property
    def real_time_consumption_enabled(self) -> bool:
        """'true' if Tibber Pulse or Watty device is paired at home"""
        return self.cache.get("realTimeConsumptionEnabled")
