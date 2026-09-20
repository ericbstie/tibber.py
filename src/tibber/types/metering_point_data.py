from __future__ import annotations

"""A class representing the MeteringPointData type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class MeteringPointData:
    """A MeteringPointData type to get information about the grid company, metering point ID and other information of a TibberHome."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def consumption_ean(self) -> str:
        """The metering point ID of the home"""
        return self.cache.get("consumptionEan")

    @property
    def grid_company(self) -> str:
        """The grid provider of the home"""
        return self.cache.get("gridCompany")

    @property
    def grid_area_code(self) -> str:
        """The grid area the home/metering point belongs to"""
        return self.cache.get("gridAreaCode")

    @property
    def price_area_code(self) -> str:
        """The price area the home/metering point belongs to"""
        return self.cache.get("priceAreaCode")

    @property
    def production_ean(self) -> str:
        """The metering point ID of the production"""
        return self.cache.get("productionEan")

    @property
    def energy_tax_type(self) -> str:
        """The eltax type of the home (only relevant for Swedish homes)"""
        return self.cache.get("energyTaxType")

    @property
    def vat_type(self) -> str:
        """The VAT type of the home (only relevant for Norwegian homes)"""
        return self.cache.get("vatType")

    @property
    def estimated_annual_consumption(self) -> int:  # pragma: no cover
        """The estimated annual consumption as reported by grid company"""
        return self.cache.get("estimatedAnnualConsumption")
