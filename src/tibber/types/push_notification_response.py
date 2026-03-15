from __future__ import annotations

"""A class representing the PushNotificationResponse type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class PushNotificationResponse:
    def __init__(self, data: dict, tibber_client: "Account"):
        self.data = data or {}  # pragma: no cover

    @property
    def successful(self):
        return self.data.get("successful")  # pragma: no cover

    @property
    def pushed_to_number_of_devices(self):
        return self.data.get("pushedToNumberOfDevices")  # pragma: no cover
