"""Tests for reading tibber.Account properties from cached values after the Tibber account is initialized."""
import pytest

import tibber
from tibber.types import NonDecoratedTibberHome
from tibber.types import Viewer
from tibber.exceptions import UnauthenticatedException


@pytest.fixture
def unfetched_account():
    return tibber.Account(tibber.DEMO_TOKEN, immediate_update=False)

def test_getting_viewer(account):
    assert isinstance(account.viewer, Viewer)

def test_getting_name(account):
    assert account.name == "Arya Stark"
    
def test_getting_login(account):
    assert account.login == "arya@winterfell.com"
    
def test_getting_user_id(account):
    assert account.user_id == "dcc2355e-6f55-45c2-beb9-274241fe450c"

def test_getting_account_type(account):
    assert account.account_type == ["customer"]
    
def test_getting_homes(account):
    assert len(account.homes) == 1
    
def test_homes_are_correct_type(account):
    assert all(isinstance(home, NonDecoratedTibberHome) for home in account.homes)

# Something wrong with pytest
# def test_incorrect_token():
#     with pytest.raises(UnauthenticatedException):
#         account = tibber.Account("invalidtoken")

def test_getting_non_fetched_property_returns_none_or_empty(unfetched_account):
    """Trying to get a value which has not yet been fetched should return None"""
    assert unfetched_account.name == None
    assert unfetched_account.viewer.homes == []

def test_set_token(account):
    assert account.token == tibber.DEMO_TOKEN
    account.token = "test"
    assert account.token == "test"

def test_setting_token_to_non_string_raises_error(account):
    with pytest.raises(TypeError):
        account.token = 105020
