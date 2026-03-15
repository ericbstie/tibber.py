from __future__ import annotations

"""A class representing the LegalEntity type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

from tibber.types.address import Address
from tibber.types.contact_info import ContactInfo

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class LegalEntity:
    """A LegalEntity (most commonly an owner of a home for example). This class contains methods to get information such as address, name and contact info."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def id(self) -> str:
        return self.cache.get("id")

    @property
    def first_name(self) -> str:
        """First/Christian name of the entity"""
        return self.cache.get("firstName")

    @property
    def is_company(self) -> bool:
        """'true' if the entity is a company"""
        return self.cache.get("isCompany")  # pragma: no cover

    @property
    def name(self) -> str:
        """Full name of the entity"""
        return self.cache.get("name")

    @property
    def middle_name(self) -> str:
        """Middle name of the entity"""
        return self.cache.get("middleName")  # pragma: no cover

    @property
    def last_name(self) -> str:
        """Last name of the entity"""
        return self.cache.get("lastName")

    @property
    def organization_no(self) -> str:
        """Organization number - only populated if entity is a company (isCompany=true)"""
        return self.cache.get("organizationNo")  # pragma: no cover

    @property
    def language(self) -> str:
        """The primary language of the entity"""
        return self.cache.get("language")  # pragma: no cover

    @property
    def contact_info(self) -> ContactInfo:
        """Contact information of the entity"""
        return ContactInfo(self.cache.get("contactInfo"), self.tibber_client)

    @property
    def address(self) -> Address:
        """Address information for the entity"""
        return Address(
            self.cache.get("address"), self.tibber_client
        )  # pragma: no cover
