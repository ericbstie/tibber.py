"""Tests for reading tibber.TibberHome properties from cached values after the Tibber account is initialized."""

from tibber.types import (
    Address,
    HomeFeatures,
    LegalEntity,
    MeteringPointData,
    Subscription,
)


def test_getting_id(home):
    assert home.id == "96a14971-525a-4420-aae9-e5aedaa129ff"


def test_getting_time_zome(home):
    assert home.time_zone == "Europe/Stockholm"


def test_getting_app_nickname(home):
    assert home.app_nickname == "Vitahuset"


def test_getting_size(home):
    assert home.size == 200


def test_getting_type(home):
    assert home.type == "HOUSE"


def test_getting_number_of_residents(home):
    assert home.number_of_residents == 5


def test_getting_primary_heating_source(home):
    assert home.primary_heating_source == "GROUND"


def test_getting_has_ventilation_system(home):
    assert not home.has_ventilation_system


def test_getting_main_fuse_size(home):
    assert home.main_fuse_size == 25


def test_getting_owner(home):
    assert isinstance(home.owner, LegalEntity)


def test_getting_metering_point_data(home):
    assert isinstance(home.metering_point_data, MeteringPointData)

    # TODO: Move to an own test file
    data = home.metering_point_data
    assert data.consumption_ean == "735999102107573183"
    assert data.grid_company == "Ellevio AB"
    assert data.grid_area_code == "STH"
    assert data.price_area_code == "SE3"
    assert data.production_ean == "735999102111362582"
    assert data.energy_tax_type == "normal"


def test_getting_current_subscription(home):
    assert isinstance(home.current_subscription, Subscription)


def test_getting_subscriptions(home):
    assert len(home.subscriptions) == 1
    assert isinstance(home.subscriptions[0], Subscription)


def test_getting_features(home):
    assert isinstance(home.features, HomeFeatures)


def test_getting_address(home):
    assert isinstance(home.address, Address)


def test_getting_address1(home):
    assert home.address1 == "Winterfell Castle 1"
