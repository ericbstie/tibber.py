"""A class for generating GraphQL queries to send to the Tibber API"""

from typing import Literal


class QueryBuilder:
    @classmethod
    def create_query_from_dict(
        cls, query_dict: dict, indentation: int = 0, last: bool = True
    ) -> str:
        """Creates a graphQL query from the keys of a dictionary.

        :param query_dict: The dictionary to convert to a query.
        :param indentation: The amount of spaces to indent the returned query.
        :param last: Specifies if the function call is the last in a recursive loop.
        """
        string_query = "{\n"

        for key, value in query_dict.items():
            if isinstance(value, dict):
                string_query += " " * (indentation + 2) + key + " "
                string_query += cls.create_query_from_dict(
                    value, indentation + 2, False
                )
                string_query += " " * (indentation + 2) + "}\n"
            else:
                string_query += " " * (indentation + 2) + key + "\n"

        if last:
            string_query += "}"

        return string_query

    @classmethod
    def create_query(cls, *args):
        """Creates a query given keys. The last argument must be a valid property of QueryBuilder that fits
        according to the GraphQL structure of the Tibber API.

        Exmaple:
            create_query("viewer", "homes", "currentSubscription", QueryBuilder.price_info())

            This returns a string query that queries specifically for the
            price_info of the current subscription in all homes.
        """
        if len(args) == 0:
            raise TypeError(
                "The QueryBuilder.create_query method requires at least one argument!"
            )

        def nest_dict(*keys):
            if len(keys) == 1:
                return keys[0]
            return {keys[0]: nest_dict(*keys[1:])}

        return QueryBuilder.create_query_from_dict(nest_dict(*args))

    @classmethod
    def combine_dicts(cls, dict1: dict, dict2: dict) -> dict:
        """Combines two nested dictionaries. The values from second dictionary overwrites the first one
        if the keys are exactly the same. The only exception to this is if the first dictionary's value
        is a dict, while the second dictionary value is a string. Then the dictionary with a dictionary
        typed value is prioritized.

        This method is meant to be used to combine query building components in dictionary form.

        :param dict1: The first dict to combine with the second dict
        :param dict2: The second dict to combine with the first dict
        :throws TypeError: If none of the parameters are dicts
        """
        if not (isinstance(dict1, dict) and isinstance(dict2, dict)):
            raise TypeError(f"Cannot combine types {type(dict1)} and {type(dict2)}.")

        result_dict = dict1

        for key, value in dict2.items():
            # The key in the second dict does not exist in the first so it's safe to add it
            # without overwriting the value from dict1 (because there is none)
            if key not in dict1.keys():
                result_dict[key] = value

            # If the value in dict1 is a string, and we know the key exists in both dict1
            # and dict2, the value from dict2 overwrite the value in dict1.
            elif isinstance(dict1[key], str):
                result_dict[key] = value

            # We know the key already exists in both dicts now. If the values in dict1 and dict 2
            # are also dicts, we need to call the function again on these dicts to resolve "merge conflicts"
            elif isinstance(value, dict):
                result_dict[key] = cls.combine_dicts(dict1[key], dict2[key])

            # We know the key exists in both dicts. If the value in dict1 is a dictionary, but
            # the value in dict2 is a string, the dict1 value is prioritized.
            elif isinstance(dict1[key], dict):
                # We can continue because the values of dict1 is already in the resulting dict
                continue

            # If the value in both dicts are strings.
            else:
                result_dict[key] = value

        return result_dict

    @classmethod
    def query_all_data(cls) -> str:
        return cls.create_query_from_dict(QueryBuilder.query())

    # -------------------------------------------------------------------
    # Query dicts for the Tibber API types. Remember that values ignored.
    # -------------------------------------------------------------------

    @classmethod
    def query(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Query` type. This type is the base type
        which all queries are nested in. Therefore, this query returns all information available from the api.
        """
        return {"viewer": QueryBuilder.viewer()}

    @classmethod
    def viewer(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Viewer` type."""
        return {
            "login": "",
            "userId": "",
            "name": "",
            "accountType": [],
            "homes": QueryBuilder.home(),
            "websocketSubscriptionUrl": "",
        }

    @classmethod
    def home(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Home` type."""
        return {
            "id": "",
            "timeZone": "",
            "appNickname": "",
            "appAvatar": "",
            "size": 0,
            "type": "",
            "numberOfResidents": 0,
            "primaryHeatingSource": "",
            "hasVentilationSystem": False,
            "mainFuseSize": 0,
            "address": QueryBuilder.address(),
            "owner": QueryBuilder.legal_entity(),
            "meteringPointData": QueryBuilder.metering_point_data(),
            "currentSubscription": QueryBuilder.subscription(),
            "subscriptions": QueryBuilder.subscription(),
            "features": QueryBuilder.features(),
        }

    @classmethod
    def address(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Address` type."""
        return {
            "address1": "",
            "address2": "",
            "address3": "",
            "city": "",
            "postalCode": "",
            "country": "",
            "latitude": "",
            "longitude": "",
        }

    @classmethod
    def legal_entity(cls) -> dict:
        """Return a dict with query values as keys for all information on the `LegalEntity` type."""
        return {
            "id": "",
            "firstName": "",
            "isCompany": False,
            "name": "",
            "middleName": "",
            "lastName": "",
            "organizationNo": "",
            "language": "",
            "contactInfo": QueryBuilder.contact_info(),
            "address": QueryBuilder.address(),
        }

    @classmethod
    def metering_point_data(cls) -> dict:
        """Return a dict with query values as keys for all information on the `MeteringPointData` type."""
        return {
            "consumptionEan": "",
            "gridCompany": "",
            "gridAreaCode": "",
            "priceAreaCode": "",
            "productionEan": "",
            "energyTaxType": "",
            "vatType": "",
            "estimatedAnnualConsumption": 0,
        }

    @classmethod
    def subscription(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Subscription` type."""
        return {
            "id": "",
            "subscriber": QueryBuilder.legal_entity(),
            "validFrom": "",
            "validTo": "",
            "status": "",
            "priceInfo": QueryBuilder.price_info(),
            "priceRating": QueryBuilder.price_rating(),
        }

    @classmethod
    def features(cls) -> dict:
        """Return a dict with query values as keys for all information on the `HomeFeatures` type."""
        return {"realTimeConsumptionEnabled": False}

    @classmethod
    def contact_info(cls) -> dict:
        """Return a dict with query values as keys for all information on the `ContactInfo` type."""
        return {"email": "", "mobile": ""}

    @classmethod
    def price_info(cls) -> dict:
        """Return a dict with query values as keys for all information on the `PriceInfo` type."""
        return {
            "current": QueryBuilder.price(),
            "today": QueryBuilder.price(),
            "tomorrow": QueryBuilder.price(),
        }

    @classmethod
    def price_rating(cls) -> dict:
        """Return a dict with query values as keys for all information on the `PriceRating` type."""
        return {
            "thresholdPercentages": QueryBuilder.price_rating_threshold_percentages(),
            "hourly": QueryBuilder.price_rating_type(),
            "daily": QueryBuilder.price_rating_type(),
            "monthly": QueryBuilder.price_rating_type(),
        }

    @classmethod
    def price(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Price` type."""
        return {
            "total": 0.0,
            "energy": 0.0,
            "tax": 0.0,
            "startsAt": "",
            "currency": "",
            "level": "",
        }

    @classmethod
    def price_rating_threshold_percentages(cls) -> dict:
        """Return a dict with query values as keys for all information on the `PriceRatingThresholdPercentages` type."""
        return {"high": 0.0, "low": 0.0}

    @classmethod
    def price_rating_type(cls) -> dict:
        """Return a dict with query values as keys for all information on the `PriceRatingType` type."""
        return {
            "minEnergy": 0.0,
            "maxEnergy": 0.0,
            "minTotal": 0.0,
            "maxTotal": 0.0,
            "currency": "",
            "entries": QueryBuilder.price_rating_entry(),
        }

    @classmethod
    def price_rating_entry(cls) -> dict:
        """Return a dict with query values as keys for all information on the `PriceRatingEntry` type."""
        return {
            "time": "",
            "energy": 0.0,
            "total": 0.0,
            "tax": 0.0,
            "difference": 0.0,
            "level": "",
        }

    # Queries with arguments. Note that these are different than queries in the way that
    # these components need to return the key for the query as well as all it's properties
    # not just the queries. This means that these should be unpacked when combined with
    # other queries, not added as a value of a key.

    @classmethod
    def single_home(home_id: str) -> dict:
        return {f"home({home_id})": QueryBuilder.home()}

    @classmethod
    def price_info_range_query(
        cls, resolution: str, first: int, last: int, before: str, after: str
    ):
        first_arg = f"first: {first}" if first else None
        last_arg = f"last: {last}" if last else None
        before_arg = f'before: "{before}"' if before else None
        after_arg = f'after: "{after}"' if after else None

        args = ", ".join(
            [
                arg
                for arg in [first_arg, last_arg, before_arg, after_arg]
                if arg is not None
            ]
        )
        return {
            f"priceInfoRange(resolution: {resolution}, {args})": {
                "pageInfo": QueryBuilder.subscription_price_connection_page_info(),
                "edges": QueryBuilder.subscription_price_edge(),
                "nodes": QueryBuilder.price(),
            }
        }

    @classmethod
    def price_info_query(cls, resolution: Literal["HOURLY", "QUARTER_HOURLY"]):
        return {
            f"priceInfo(resolution: {resolution})": {
                "current": QueryBuilder.price(),
                "today": QueryBuilder.price(),
                "tomorrow": QueryBuilder.price(),
            }
        }

    @classmethod
    def range_query(
        cls, resolution: str, first: int, last: int, before: str, after: str
    ):
        first_arg = f"first: {first}" if first else None
        last_arg = f"last: {last}" if last else None
        before_arg = f'before: "{before}"' if before else None
        after_arg = f'after: "{after}"' if after else None

        args = ", ".join(
            [
                arg
                for arg in [first_arg, last_arg, before_arg, after_arg]
                if arg is not None
            ]
        )
        return {
            f"range(resolution: {resolution}, {args})": {
                "pageInfo": QueryBuilder.subscription_price_connection_page_info(),
                "edges": QueryBuilder.subscription_price_edge(),
                "nodes": QueryBuilder.price(),
            }
        }

    @classmethod
    def consumption_query(
        cls,
        resolution: str,
        first: int = None,
        last: int = None,
        before: str = None,
        after: str = None,
        filter_empty_nodes: bool = False,
    ):
        # TODO: I feel like this can be improved...
        first_arg = f"first: {first}" if first else ""
        last_arg = f"last: {last}" if last else ""
        before_arg = f'before: "{before}"' if before else ""
        after_arg = f'after: "{after}"' if after else ""

        args = ", ".join(
            [arg for arg in [first_arg, last_arg, before_arg, after_arg] if arg]
        )
        return {
            f"consumption(resolution: {resolution}, {args}, filterEmptyNodes: {str(filter_empty_nodes).lower()})": {
                "pageInfo": QueryBuilder.home_consumption_page_info(),
                "nodes": QueryBuilder.consumption(),
                "edges": QueryBuilder.home_consumption_edge(),
            }
        }

    @classmethod
    def production_query(
        cls,
        resolution: str,
        first: int = None,
        last: int = None,
        before: str = None,
        after: str = None,
        filter_empty_nodes: bool = False,
    ):
        first_arg = f"first: {first}" if first else ""
        last_arg = f"last: {last}" if last else ""
        before_arg = f'before: "{before}"' if before else ""
        after_arg = f'after: "{after}"' if after else ""

        args = ", ".join(
            [arg for arg in [first_arg, last_arg, before_arg, after_arg] if arg]
        )
        return {
            f"production(resolution: {resolution}, {args}, filterEmptyNodes: {str(filter_empty_nodes).lower()})": {
                "pageInfo": QueryBuilder.home_production_page_info(),
                "nodes": QueryBuilder.production(),
                "edges": QueryBuilder.home_production_edge(),
            }
        }

    @classmethod
    def home_consumption_page_info(cls):
        return {
            "endCursor": "",
            "hasNextPage": False,
            "hasPreviousPage": False,
            "startCursor": "",
            "count": 0,
            "currency": "",
            "totalCost": 0.0,
            "totalConsumption": 0.0,
            "filtered": 0,
        }

    @classmethod
    def consumption(cls):
        return {
            "from": "",
            "to": "",
            "unitPrice": 0.0,
            "unitPriceVAT": 0.0,
            "consumption": 0.0,
            "consumptionUnit": "",
            "cost": 0.0,
            "currency": "",
        }

    @classmethod
    def home_consumption_edge(cls):
        return {"cursor": "", "node": QueryBuilder.consumption()}

    @classmethod
    def home_production_page_info(cls):
        return {
            "endCursor": "",
            "hasNextPage": False,
            "hasPreviousPage": False,
            "startCursor": "",
            "count": 0,
            "currency": "",
            "totalProfit": 0.0,
            "totalProduction": 0.0,
            "filtered": 0,
        }

    @classmethod
    def production(cls):
        return {
            "from": "",
            "to": "",
            "unitPrice": 0.0,
            "unitPriceVAT": 0.0,
            "production": 0.0,
            "productionUnit": "",
            "profit": 0.0,
            "currency": "",
        }

    @classmethod
    def home_production_edge(cls):
        return {"cursor": "", "node": QueryBuilder.production()}

    @classmethod
    def subscription_price_connection_page_info(cls):
        return {
            "endCursor": "",
            "hasNextPage": False,
            "hasPreviousPage": False,
            "startCursor": "",
            "resolution": "",
            "currency": "",
            "count": 0,
            "precision": "",
            "minEnergy": 0.0,
            "minTotal": 0.0,
            "maxEnergy": 0.0,
            "maxTotal": 0.0,
        }

    @classmethod
    def subscription_price_edge(cls):
        return {
            "cursor": "",
            "node": QueryBuilder.price(),
        }

    # Live data - This WILL be rewritten together with this whole class.
    # TODO: Rewrite the whole class from a dict-based approach to a string-based approach.
    @classmethod
    def live_measurement(cls, home_id):
        return f"""subscription {{
            liveMeasurement(homeId: "{home_id}") {{
                timestamp
                power
                lastMeterConsumption
                accumulatedConsumption
                accumulatedProduction
                accumulatedConsumptionLastHour
                accumulatedProductionLastHour
                accumulatedCost
                accumulatedReward
                currency
                minPower
                averagePower
                maxPower
                powerProduction
                powerReactive
                powerProductionReactive
                minPowerProduction
                maxPowerProduction
                lastMeterProduction
                powerFactor
                voltagePhase1
                voltagePhase2
                voltagePhase3
                currentL1
                currentL2
                currentL3
                signalStrength
            }}
        }}"""

    @classmethod
    def send_push_notification(
        cls, title: str, message: str, screen_to_open: str = None
    ):
        return f"""mutation {{
            sendPushNotification(input: {{
                title: "{title}",
                message: "{message}",
                {'screenToOpen: ' + screen_to_open if screen_to_open else ""}
            }}) {{
                successful
                pushedToNumberOfDevices
            }}
        }}"""
