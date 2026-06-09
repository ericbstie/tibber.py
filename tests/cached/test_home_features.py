"""Tests to verify home features data"""


def test_real_time_consumption(home):
    assert home.features.real_time_consumption_enabled
