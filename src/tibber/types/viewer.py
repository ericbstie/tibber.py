from __future__ import annotations

"""A class representing the Viewer type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

from tibber.types.home import TibberHome

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class Viewer:
    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def name(self):
        return self.cache.get("name")

    @property
    def login(self):
        return self.cache.get("login")

    @property
    def user_id(self):
        """Unique user identifier"""
        return self.cache.get("userId")

    @property
    def account_type(self):
        """The type of account for the logged-in user."""
        return self.cache.get("accountType")

    @property
    def homes(self):
        """All homes visible to the logged-in user"""
        return [
            TibberHome(home, self.tibber_client) for home in self.cache.get("homes", [])
        ]

    @property
    def websocket_subscription_url(self):
        """The URL to use for websocket subscriptions"""
        return self.cache.get("websocketSubscriptionUrl")

    # TODO: Implement home(id: ID!): Home! method. (get_home and fetch_home)
