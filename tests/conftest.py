import json

import pytest

import tibber


@pytest.fixture(scope="session")
def account():
    try:
        account = tibber.Account(tibber.DEMO_TOKEN)
        assert True
    except Exception as e:
        print(e)
        print("############ USING BACKUP SAMPLE DATA INSTEAD ############")
        account = tibber.Account(tibber.DEMO_TOKEN, immediate_update=False)
        with open("./tests/backup_demo_data.json", "r") as f:
            data = json.load(f)
        account.update_cache(data)

    return account


@pytest.fixture(scope="session")
def home(account):
    try:
        return account.homes[0]
    except IndexError:
        raise ValueError(
            "The instanciated demo account does not have any homes. Cannot perform home tests."
        )
