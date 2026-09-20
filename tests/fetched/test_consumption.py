"""Tests for fetching consumption data from the API."""


def test_consumption_page_info(home):
    home_consumption_connection = home.fetch_consumption(
        "HOURLY", first=5, after="MjAyMy0wMi0wNlQwMTowMDowMC4wMDArMDE6MDA="
    )
    page_info = home_consumption_connection.page_info

    assert page_info.end_cursor == home_consumption_connection.edges[-1].cursor
    assert page_info.has_next_page
    assert page_info.has_previous_page
    assert page_info.start_cursor == home_consumption_connection.edges[0].cursor

    assert page_info.count == 5
    assert page_info.currency == "SEK"
    assert page_info.total_cost == 25.4909709625
    assert page_info.total_consumption == 16.633
    assert page_info.filtered == 0


def test_consumption_nodes(home):
    home_consumption_connection = home.fetch_consumption(
        "HOURLY", first=3, after="MjAyMy0wMi0wNlQwMTowMDowMC4wMDArMDE6MDA="
    )
    history = home_consumption_connection.nodes

    assert history[0].from_time == "2023-02-06T01:00:00.000+01:00"
    assert history[0].to_time == "2023-02-06T02:00:00.000+01:00"

    assert [node.cost for node in history] == [3.8449054875, 4.416853275, 5.561462025]
    assert [node.unit_price for node in history] == [1.3290375, 1.2455875, 1.401225]
    assert [node.unit_price_vat for node in history] == [0.2658075, 0.2491175, 0.280245]
    assert [node.consumption for node in history] == [2.893, 3.546, 3.969]
    assert all(node.consumption_unit == "kWh" for node in history)
