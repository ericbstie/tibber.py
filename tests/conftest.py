"""Shared fixtures for the test suite.

The default test suite runs fully offline: the account fixture is preloaded with
recorded demo data and never opens a network connection. Tests that require the real
Tibber API are marked "live" or "realtime" and are deselected by default (see the
pytest configuration in pyproject.toml). Run them with:

    uv run pytest -m "live or realtime"
"""

import json
from pathlib import Path
from unittest import mock

import pytest

import tibber
from tibber.networking import QueryExecutor

SAMPLE_DATA_FILE = Path(__file__).parent / "backup_demo_data.json"


async def _offline_ainit(self, session):
    """Replacement for QueryExecutor.__ainit__ that skips connecting to the API."""
    self.session = session


def create_offline_account() -> tibber.Account:
    """Create an Account without opening any network connection.

    Queries executed later (e.g. by tests marked "live") still work: the gql client
    connects on demand for each query.
    """
    with mock.patch.object(QueryExecutor, "__ainit__", _offline_ainit):
        return tibber.Account(tibber.DEMO_TOKEN, immediate_update=False)


@pytest.fixture(scope="session")
def sample_data() -> dict:
    """Recorded demo account data, as returned by Account.fetch_all()."""
    with open(SAMPLE_DATA_FILE) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def account(sample_data):
    """An Account preloaded with the recorded demo data. Does not touch the network."""
    account = create_offline_account()
    account.update_cache(sample_data)
    return account


@pytest.fixture
def unfetched_account():
    """An Account with an empty cache. Does not touch the network."""
    return create_offline_account()


@pytest.fixture(scope="session")
def home(account):
    try:
        return account.homes[0]
    except IndexError as e:
        raise ValueError(
            "The recorded demo account data does not contain any homes. "
            "Cannot perform home tests."
        ) from e
