"""Offline tests locking the exact GraphQL queries QueryBuilder generates.

These are golden tests: they assert the exact output strings so that internal
refactors of the query building logic cannot silently change the queries sent to
the Tibber API.
"""
import pytest

from tibber.networking import QueryBuilder


def test_create_query_from_dict_renders_nested_keys():
    query = QueryBuilder.create_query_from_dict({"a": "", "b": {"c": ""}})
    assert query == "{\n  a\n  b {\n    c\n  }\n}"


def test_create_query_requires_at_least_one_argument():
    with pytest.raises(TypeError):
        QueryBuilder.create_query()


def test_create_query_nests_arguments():
    query = QueryBuilder.create_query(
        "viewer", 'home(id: "abc")', {"appNickname": ""}
    )
    assert query == (
        "{\n"
        "  viewer {\n"
        '    home(id: "abc") {\n'
        "      appNickname\n"
        "    }\n"
        "  }\n"
        "}"
    )


def test_query_all_data_queries_the_full_viewer():
    query = QueryBuilder.query_all_data()
    for expected_field in ["viewer", "homes", "currentSubscription", "priceInfo"]:
        assert expected_field in query


class TestCombineDicts:
    def test_merges_nested_dicts(self):
        result = QueryBuilder.combine_dicts(
            {"a": "", "b": {"c": ""}}, {"b": {"d": ""}, "e": ""}
        )
        assert result == {"a": "", "b": {"c": "", "d": ""}, "e": ""}

    def test_dict_value_overwrites_string_value(self):
        assert QueryBuilder.combine_dicts({"a": ""}, {"a": {"x": ""}}) == {"a": {"x": ""}}

    def test_dict_value_is_kept_over_string_value(self):
        assert QueryBuilder.combine_dicts({"a": {"x": ""}}, {"a": ""}) == {"a": {"x": ""}}

    def test_second_string_value_wins(self):
        assert QueryBuilder.combine_dicts({"a": "1"}, {"a": "2"}) == {"a": "2"}

    def test_non_dicts_raise_type_error(self):
        with pytest.raises(TypeError):
            QueryBuilder.combine_dicts("a", {"b": ""})


class TestPaginationArguments:
    """The exact argument rendering of every paginated query."""

    def test_consumption_query_with_first(self):
        keys = list(QueryBuilder.consumption_query("HOURLY", first=2).keys())
        assert keys == ["consumption(resolution: HOURLY, first: 2, filterEmptyNodes: false)"]

    def test_consumption_query_with_last_before_and_filter(self):
        keys = list(
            QueryBuilder.consumption_query(
                "DAILY", last=3, before="abc", filter_empty_nodes=True
            ).keys()
        )
        assert keys == ['consumption(resolution: DAILY, last: 3, before: "abc", filterEmptyNodes: true)']

    def test_production_query_with_first_and_after(self):
        keys = list(QueryBuilder.production_query("HOURLY", first=1, after="xyz").keys())
        assert keys == ['production(resolution: HOURLY, first: 1, after: "xyz", filterEmptyNodes: false)']

    def test_range_query(self):
        keys = list(QueryBuilder.range_query("DAILY", 2, None, None, "abc").keys())
        assert keys == ['range(resolution: DAILY, first: 2, after: "abc")']

    def test_price_info_range_query(self):
        keys = list(
            QueryBuilder.price_info_range_query("QUARTER_HOURLY", 10, None, None, "abc").keys()
        )
        assert keys == ['priceInfoRange(resolution: QUARTER_HOURLY, first: 10, after: "abc")']

    def test_price_info_query(self):
        keys = list(QueryBuilder.price_info_query("HOURLY").keys())
        assert keys == ["priceInfo(resolution: HOURLY)"]

    def test_paginated_queries_request_page_info_nodes_and_edges(self):
        for query_dict in [
            QueryBuilder.consumption_query("HOURLY", first=1),
            QueryBuilder.production_query("HOURLY", first=1),
            QueryBuilder.range_query("HOURLY", 1, None, None, None),
            QueryBuilder.price_info_range_query("HOURLY", 1, None, None, None),
        ]:
            (fields,) = query_dict.values()
            assert {"pageInfo", "nodes", "edges"} <= set(fields)


def test_live_measurement_subscription_query():
    query = QueryBuilder.live_measurement("home-id-123")
    assert query.lstrip().startswith("subscription {")
    assert 'liveMeasurement(homeId: "home-id-123")' in query
    for field in ["timestamp", "power", "accumulatedCost", "currency", "signalStrength"]:
        assert field in query


def test_send_push_notification_without_screen_to_open():
    query = QueryBuilder.send_push_notification("Title", "Message")
    assert 'title: "Title",' in query
    assert 'message: "Message",' in query
    assert "screenToOpen" not in query


def test_send_push_notification_with_screen_to_open():
    query = QueryBuilder.send_push_notification("Title", "Message", "HOME")
    assert "screenToOpen: HOME" in query
