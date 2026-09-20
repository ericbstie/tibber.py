"""Tests fetching historical price data."""

import base64
from datetime import datetime, timedelta, timezone

import pytest


def encode_date(date: datetime) -> str:
    return base64.b64encode(date.astimezone().isoformat().encode("utf-8")).decode(
        "utf-8"
    )


def test_fetching_hourly_prices(home):
    date = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=1)))

    data = home.current_subscription.fetch_price_info_range(
        "HOURLY", first="3", after=encode_date(date)
    )

    assert data.page_info.count == 3
    assert len(data.nodes) == 3

    assert data.nodes[0].starts_at == "2025-01-01T00:00:00.000+01:00"
    assert data.nodes[1].starts_at == "2025-01-01T01:00:00.000+01:00"
    assert data.nodes[2].starts_at == "2025-01-01T02:00:00.000+01:00"


def test_fetching_quarter_hourly_prices(home):
    date = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=1)))

    data = home.current_subscription.fetch_price_info_range(
        "QUARTER_HOURLY", first="4", after=encode_date(date)
    )

    assert data.page_info.count == 4
    assert len(data.nodes) == 4

    assert data.nodes[0].starts_at == "2025-01-01T00:00:00.000+01:00"
    assert data.nodes[1].starts_at == "2025-01-01T00:15:00.000+01:00"
    assert data.nodes[2].starts_at == "2025-01-01T00:30:00.000+01:00"
    assert data.nodes[3].starts_at == "2025-01-01T00:45:00.000+01:00"


def test_deprecated_fetch_range_warns_and_delegates(home):
    date = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=1)))

    with pytest.warns(DeprecationWarning, match="fetch_price_info_range"):
        data = home.current_subscription.price_info.fetch_range(
            "HOURLY", first="3", after=encode_date(date)
        )

    assert data.page_info.count == 3
    assert len(data.nodes) == 3

    assert data.nodes[0].starts_at == "2025-01-01T00:00:00.000+01:00"
    assert data.nodes[1].starts_at == "2025-01-01T01:00:00.000+01:00"
    assert data.nodes[2].starts_at == "2025-01-01T02:00:00.000+01:00"
