from __future__ import annotations

"""A class representing the Address type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class Address:
    """An address type to get information about the location of a TibberHome."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def address1(self) -> str:
        return self.cache.get("address1")

    @property
    def address2(self) -> str:
        return self.cache.get("address2")  # pragma: no cover

    @property
    def address3(self) -> str:
        return self.cache.get("address3")  # pragma: no cover

    @property
    def city(self) -> str:
        return self.cache.get("city")  # pragma: no cover

    @property
    def postal_code(self) -> str:
        return self.cache.get("postalCode")  # pragma: no cover

    @property
    def country(self) -> str:
        return self.cache.get("country")  # pragma: no cover

    @property
    def latitude(self) -> str:
        return self.cache.get("latitude")  # pragma: no cover

    @property
    def longitude(self) -> str:
        return self.cache.get("longitude")  # pragma: no cover
