from __future__ import annotations

"""A class representing the SubscriptionPriceConnection type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

from tibber.types.price import Price
from tibber.types.subscription_price_edge import SubscriptionPriceEdge

from tibber.types.subscription_price_connection_page_info import (  # isort:skip
    SubscriptionPriceConnectionPageInfo,
)

if TYPE_CHECKING:
    from tibber.account import Account


class SubscriptionPriceConnection:
    """A class to get subscription price connection."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def edges(self) -> list[SubscriptionPriceEdge]:
        return [
            SubscriptionPriceEdge(edge, self.tibber_client)
            for edge in self.cache.get("edges", [])
        ]

    @property
    def page_info(self) -> SubscriptionPriceConnectionPageInfo:
        return SubscriptionPriceConnectionPageInfo(
            self.cache.get("pageInfo"), self.tibber_client
        )

    @property
    def nodes(self) -> list[Price]:
        """List of Price objects from the executed range query."""
        return [Price(node, self.tibber_client) for node in self.cache.get("nodes", [])]
