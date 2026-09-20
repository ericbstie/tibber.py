from __future__ import annotations

"""A class representing the HomeProductionEdge type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

from tibber.types.production import Production

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class HomeProductionEdge:
    """A class containing household electricity production information for a time period."""

    def __init__(self, resolution: str, data: dict, tibber_client: "Account"):
        self.resolution = resolution
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def cursor(self) -> str:
        return self.cache.get("cursor")

    @property
    def node(self) -> Production:
        return Production(self.cache.get("node"), self.tibber_client)
