"""Tests for reading live data from a tibber.TibberHome"""
import pytest
from datetime import datetime
from datetime import timedelta

import tibber
from tibber import __version__
from tibber.types.live_measurement import LiveMeasurement

pytestmark = pytest.mark.realtime


@pytest.mark.timeout(60)
def test_starting_live_feed_with_no_listeners_shows_warning(caplog):
    account = tibber.Account(tibber.DEMO_TOKEN)
    home = account.homes[0]

    # Return immediately after the first callback
    home.start_live_feed(f"tibber.py-tests/{__version__}", exit_condition = lambda data: True)
    assert "The event that was broadcasted has no listeners / callbacks! Nothing was run." in caplog.text

@pytest.mark.timeout(60)
def test_retrieving_live_measurements():
    account = tibber.Account(tibber.DEMO_TOKEN)
    home = account.homes[0]

    global callback_was_run
    callback_was_run = False

    @home.event("live_measurement")
    async def callback(data):
        global callback_was_run
        callback_was_run = True
        assert isinstance(data, LiveMeasurement)
        timestamp = datetime.strptime(data.timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        timestamp = timestamp.replace(tzinfo=None)
        now = datetime.now().replace(tzinfo=None)
        assert timestamp > now - timedelta(seconds=30)

    # Return immediately after the first callback
    home.start_live_feed(f"tibber.py-tests/{__version__}", exit_condition = lambda data: True)
    assert callback_was_run
