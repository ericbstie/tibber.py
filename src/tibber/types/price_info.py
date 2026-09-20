from __future__ import annotations

"""A class representing the PriceInfo type from the GraphQL Tibber API."""
import warnings
from typing import TYPE_CHECKING, Optional

from tibber.networking.query_builder import QueryBuilder
from tibber.types.price import Price

from tibber.types.subscription_price_connection import (  # isort: skip
    SubscriptionPriceConnection,
)

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class PriceInfo:
    """A class to get price info."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def current(self) -> Price:
        """The energy price right now"""
        return Price(self.cache.get("current"), self.tibber_client)

    @property
    def today(self) -> list[Price]:
        """The hourly prices of the current day"""
        return [Price(hour, self.tibber_client) for hour in self.cache.get("today", [])]

    @property
    def tomorrow(self) -> list[Price]:
        """The hourly prices of the upcoming day"""
        return [
            Price(hour, self.tibber_client) for hour in self.cache.get("tomorrow", [])
        ]

    def fetch_range(
        self,
        resolution: str,
        first: Optional[str] = None,
        last: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        home_id: Optional[str] = None,
    ) -> SubscriptionPriceConnection:
        """Fetch the price range.

        .. deprecated::
            The underlying `PriceInfo.range` field is deprecated by the Tibber API
            (moved to `Subscription.priceInfoRange` with the introduction of
            quarter hourly prices on October 1st, 2025). Use
            `Subscription.fetch_price_info_range` instead.

        The before and after arguments are Base64 encoded ISO 8601 datetimes."""
        warnings.warn(
            "PriceInfo.fetch_range is deprecated because the Tibber API deprecated "
            "the underlying PriceInfo.range field. "
            "Use Subscription.fetch_price_info_range instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        price_info_range_query_dict = QueryBuilder.price_info_range_query(
            resolution, first, last, before, after
        )

        price_info_range_query = QueryBuilder.create_query(
            "viewer", "homes", "currentSubscription", price_info_range_query_dict
        )
        full_data = self.tibber_client.execute_query(
            self.tibber_client.token, price_info_range_query
        )

        home = full_data["viewer"]["homes"][0]
        if home_id:
            home_of_id = [
                home for home in full_data["viewer"]["homes"] if home["id"] == home_id
            ][0]

            if home_of_id:
                home = home_of_id

        return SubscriptionPriceConnection(
            home["currentSubscription"]["priceInfoRange"], self.tibber_client
        )
