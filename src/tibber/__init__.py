__version__ = "0.7.1"
DEMO_TOKEN = "3A77EECF61BD445F47241A5A36202185C35AF3AF58609E19B53F3A8872AD7BE1-1"
API_ENDPOINT = "https://api.tibber.com/v1-beta/gql"

import asyncio
import os

# The event loop type causes problems on windows systems when exiting.
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Import modules after defining constants to avoid circular import error.
from .account import Account
from .types.home import NonDecoratedTibberHome, TibberHome

__all__ = [
    "__version__",
    "DEMO_TOKEN",
    "API_ENDPOINT",
    "Account",
    "NonDecoratedTibberHome",
    "TibberHome",
]
