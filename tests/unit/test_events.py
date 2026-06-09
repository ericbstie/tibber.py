"""Offline tests for the live measurement event registration and broadcasting."""
import asyncio

import pytest

from tibber.types.home import TibberHome


@pytest.fixture
def fresh_home(account):
    """A TibberHome with its own (empty) callback registry."""
    return TibberHome(account.homes[0].cache, account)


def test_adding_listener_with_unknown_event_raises_exception(fresh_home):
    with pytest.raises(ValueError):
        @fresh_home.event("invalid-event-name")
        async def callback(data):
            print(data)


def test_adding_non_coroutine_listener_raises_exception(fresh_home):
    with pytest.raises(ValueError):
        @fresh_home.event("live_measurement")
        def callback(data):
            print(data)


def test_event_decorator_returns_the_callback(fresh_home):
    async def callback(data):
        pass

    assert fresh_home.event("live_measurement")(callback) is callback


def test_broadcast_runs_all_registered_callbacks(fresh_home):
    calls = []

    @fresh_home.event("live_measurement")
    async def first_callback(data):
        calls.append(("first", data))

    @fresh_home.event("live_measurement")
    async def second_callback(data):
        calls.append(("second", data))

    asyncio.run(fresh_home.broadcast_event("live_measurement", "payload"))
    assert ("first", "payload") in calls
    assert ("second", "payload") in calls


def test_broadcast_without_listeners_warns(fresh_home, caplog):
    asyncio.run(fresh_home.broadcast_event("live_measurement", None))
    assert "no listeners" in caplog.text
