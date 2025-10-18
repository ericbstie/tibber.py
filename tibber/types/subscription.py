from __future__ import annotations

"""A class representing the Subscription type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING, Literal, Optional

from tibber.networking.query_builder import QueryBuilder
from tibber.types.legal_entity import LegalEntity
from tibber.types.price_info import PriceInfo
from tibber.types.price_rating import PriceRating
from tibber.types.subscription_price_connection import SubscriptionPriceConnection

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class Subscription:
    """A class to get information about the subscription of a TibberHome."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def id(self) -> str:
        return self.cache.get("id")

    @property
    def subscriber(self) -> LegalEntity:
        """The owner of the subscription"""
        return LegalEntity(self.cache.get("subscriber"), self.tibber_client)

    @property
    def valid_from(self) -> str:
        """The time the subscription started"""
        return self.cache.get("validFrom")

    @property
    def valid_to(self) -> str:
        """The time the subscription ended"""
        return self.cache.get("validTo")

    @property
    def status(self) -> str:
        """The current status of the subscription"""
        return self.cache.get("status")

    @property
    def price_info(self) -> PriceInfo:
        """Price information related to the subscription"""
        return PriceInfo(self.cache.get("priceInfo"), self.tibber_client)

    def fetch_price_info(
        self,
        resolution: Literal["HOURLY", "QUARTER_HOURLY"],
        home_id: Optional[str] = None,
    ) -> PriceInfo:
        price_info_query_dict = QueryBuilder.price_info_query(resolution)

        price_info_query = QueryBuilder.create_query(
            "viewer", "homes", "currentSubscription", price_info_query_dict
        )

        full_data = self.tibber_client.execute_query(
            self.tibber_client.token, price_info_query
        )

        home = full_data["viewer"]["homes"][0]
        if home_id:
            home_of_id = [
                home for home in full_data["viewer"]["homes"] if home["id"] == home_id
            ][0]

            if home_of_id:
                home = home_of_id

        return PriceInfo(home["currentSubscription"]["priceInfo"], self.tibber_client)

    def fetch_price_info_range(
        self,
        resolution: str,
        first: Optional[str] = None,
        last: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        home_id: Optional[str] = None,
    ) -> SubscriptionPriceConnection:
        """Fetch PriceInfo for a given range.

        The before and after arguments are Base64 encoded ISO 8601 datetimes."""
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

    @property
    def price_rating(self) -> PriceRating:
        """Price information related to the subscription"""
        return PriceRating(self.cache.get("priceRating"), self.tibber_client)
