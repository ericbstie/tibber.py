from __future__ import annotations

"""A class representing the Production type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class Production:
    """A class containing concrete household electricity production information for a time period."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def from_time(self) -> str:
        return self.cache.get("from")

    @property
    def to_time(self) -> str:
        return self.cache.get("to")

    @property
    def unit_price(self) -> float:
        return self.cache.get("unitPrice")

    @property
    def unit_price_vat(self) -> float:
        return self.cache.get("unitPriceVAT")

    @property
    def production(self) -> float:
        """kWh produced"""  # Docs actually say consumed here, but I assume it means to say produced
        return self.cache.get("production")

    @property
    def production_unit(self) -> str:
        return self.cache.get("productionUnit")

    @property
    def profit(self) -> float:
        """Total profit of the production"""
        return self.cache.get("profit")

    @property
    def currency(self) -> str:
        """The cost currency"""
        return self.cache.get("currency")
