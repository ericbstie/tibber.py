from __future__ import annotations

"""A class representing the PriceRating type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

from tibber.types.price_rating_type import PriceRatingType

from tibber.types.price_rating_threshold_percentages import (  # isort:skip
    PriceRatingThresholdPercentages,
)

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class PriceRating:
    """A class to get the rating of a price in relative terms."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def threshold_percentages(self) -> dict:
        """The different 'high'/'low' price breakpoints (market dependent)"""
        return PriceRatingThresholdPercentages(
            self.cache.get("thresholdPercentages"), self.tibber_client
        )

    @property
    def hourly(self) -> dict:
        """The hourly prices of today, the previous 7 days, and tomorrow"""
        return PriceRatingType(self.cache.get("hourly"), self.tibber_client)

    @property
    def daily(self) -> dict:
        """The daily prices of today and the previous 30 days"""
        return PriceRatingType(self.cache.get("daily"), self.tibber_client)

    @property
    def monthly(self) -> dict:
        """The monthly prices of this month and the previous 31 months"""
        return PriceRatingType(self.cache.get("monthly"), self.tibber_client)
