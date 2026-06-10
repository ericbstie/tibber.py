"""Tests that the sync API is a thin facade over the async core and works
from any calling context, including inside a running event loop (issue #65)."""

import asyncio

import tibber


def test_account_can_be_created_inside_a_running_event_loop():
    async def main():
        return tibber.Account(tibber.DEMO_TOKEN)

    account = asyncio.run(main())
    assert account.name == "Arya Stark"


def test_sync_fetch_works_inside_a_running_event_loop(home):
    async def main():
        return home.fetch_consumption("HOURLY", first=2)

    data = asyncio.run(main())
    assert len(data.nodes) == 2


def test_sync_fetch_price_info_works_inside_a_running_event_loop(home):
    """The exact scenario reported in issue #65."""

    async def main():
        return home.current_subscription.fetch_price_info("HOURLY")

    price_info = asyncio.run(main())
    assert len(price_info.today) > 0


def test_update_async_still_works_from_a_user_event_loop(account):
    async def main():
        await account.update_async()

    asyncio.run(main())
    assert account.name == "Arya Stark"
