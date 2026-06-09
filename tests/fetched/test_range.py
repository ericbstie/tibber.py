"""Tests fetching historical price data."""

import base64
from datetime import datetime, timedelta, timezone


def test_fetching_hourly_prices(home):
    date = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=1)))
    encoded = base64.b64encode(date.astimezone().isoformat().encode("utf-8")).decode(
        "utf-8"
    )

    data = home.current_subscription.price_info.fetch_range(
        "HOURLY", first="3", after=encoded
    )

    assert data.page_info.count == 3
    assert len(data.nodes) == 3

    assert data.nodes[0].starts_at == "2025-01-01T00:00:00.000+01:00"
    assert data.nodes[1].starts_at == "2025-01-01T01:00:00.000+01:00"
    assert data.nodes[2].starts_at == "2025-01-01T02:00:00.000+01:00"
