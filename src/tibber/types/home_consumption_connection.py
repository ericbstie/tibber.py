from __future__ import annotations

"""A class representing the HomeConsumptionConnection type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

from tibber.types.consumption import Consumption
from tibber.types.home_consumption_edge import HomeConsumptionEdge
from tibber.types.home_consumption_page_info import HomeConsumptionPageInfo

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class HomeConsumptionConnection:
    """A class containing household electricity consumption information for a time period."""

    def __init__(self, resolution: str, data: dict, tibber_client: "Account"):
        self.resolution = resolution
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def page_info(self) -> str:
        return HomeConsumptionPageInfo(
            self.resolution, self.cache.get("pageInfo"), self.tibber_client
        )

    @property
    def nodes(self) -> list:
        return [
            Consumption(node, self.tibber_client) for node in self.cache.get("nodes")
        ]

    @property
    def edges(self) -> list:
        return [
            HomeConsumptionEdge(self.resolution, edge, self.tibber_client)
            for edge in self.cache.get("edges")
        ]

    def __iter__(self):
        return iter(self.nodes)
