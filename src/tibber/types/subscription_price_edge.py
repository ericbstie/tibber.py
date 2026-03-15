from __future__ import annotations

"""A class representing the SubscriptionPriceEdge type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

from tibber.types.price import Price

if TYPE_CHECKING:
    from tibber.account import Account


class SubscriptionPriceEdge:
    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def cursor(self) -> str:
        return self.cache.get("cursor")

    @property
    def node(self) -> Price:
        return Price(self.cache.get("node"), self.tibber_client)
