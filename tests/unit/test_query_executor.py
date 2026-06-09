"""Offline tests for error handling and caching in the query executor / account."""
import pytest

from tibber.exceptions import APIException, UnauthenticatedException


def test_unauthenticated_error_raises_unauthenticated_exception(unfetched_account):
    error = {
        "message": "invalid token",
        "extensions": {"code": "UNAUTHENTICATED"},
    }
    with pytest.raises(UnauthenticatedException, match="invalid token"):
        unfetched_account._process_error(error)


def test_other_error_codes_raise_api_exception(unfetched_account):
    error = {
        "message": "something else went wrong",
        "extensions": {"code": "INTERNAL_SERVER_ERROR"},
    }
    with pytest.raises(APIException):
        unfetched_account._process_error(error)


def test_malformed_error_raises_api_exception(unfetched_account):
    with pytest.raises(APIException):
        unfetched_account._process_error({"unexpected": "shape"})


def test_setting_token_to_non_string_raises_type_error(unfetched_account):
    with pytest.raises(TypeError):
        unfetched_account.token = 42


def test_setting_token_to_string_updates_token(unfetched_account):
    unfetched_account.token = "new-token"
    assert unfetched_account.token == "new-token"


def test_update_cache_merges_new_data(unfetched_account):
    unfetched_account.update_cache({"viewer": {"name": "Arya Stark"}})
    unfetched_account.update_cache({"viewer": {"login": "arya@winterfell.com"}})
    assert unfetched_account.cache == {
        "viewer": {"name": "Arya Stark", "login": "arya@winterfell.com"}
    }
    assert unfetched_account.name == "Arya Stark"
    assert unfetched_account.login == "arya@winterfell.com"
