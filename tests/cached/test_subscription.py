"""Tests for reading tibber.types.Subscription properties from cached values after the Tibber account is initialized."""

import pytest

from tibber.types import LegalEntity, PriceInfo, PriceRating, Subscription


@pytest.fixture
def subscription(home):
    return home.current_subscription


def test_correct_type(subscription):
    assert isinstance(subscription, Subscription)


def test_getting_id(subscription):
    assert subscription.id == "a386fd22-579e-4364-8b17-c63bef0d6bee"


def test_getting_subscriber(subscription):
    assert isinstance(subscription.subscriber, LegalEntity)


def test_getting_valid_from(subscription):
    assert subscription.valid_from == "2018-11-01T23:00:00+00:00"


def test_getting_status(subscription):
    assert subscription.status == "running"


def test_getting_price_info(subscription):
    assert isinstance(subscription.price_info, PriceInfo)


def test_getting_price_rating(subscription):
    assert isinstance(subscription.price_rating, PriceRating)
