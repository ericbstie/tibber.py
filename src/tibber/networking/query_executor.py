import asyncio
import logging

import asyncio_atexit
import backoff
import gql
import websockets
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

from tibber import API_ENDPOINT
from tibber.exceptions import APIException, UnauthenticatedException

_logger = logging.getLogger(__name__)


class QueryExecutor:
    """A class for executing queries."""

    def __init__(self, session=None, transport_kwargs={}):
        self.gql_client = None
        transport = AIOHTTPTransport(
            url=API_ENDPOINT,
            headers={"Authorization": "Bearer " + self.token},
            ssl=True,
            **transport_kwargs,
        )
        self.gql_client = gql.Client(
            transport=transport, fetch_schema_from_transport=True
        )

        asyncio.run(self.__ainit__(session))

    async def __ainit__(self, session):
        self.session = session or await self.gql_client.connect_async()
        asyncio_atexit.register(self.gql_client.close_async)

    def execute_query(
        self, access_token: str, query: str, max_tries: int = 1, **kwargs
    ):
        """Executes a GraphQL query to the Tibber API.

        :param access_token: The Tibber API token to use for the request.
        :param query: The query to send to the Tibber API.
        :param max_tries: The amount of attempts before giving up. Set to None for infinite tries.
        :param **kwargs: Arguments to be passed in to the backoff.on_exception decorator
        """
        # To allow invocations from async contexts, check if a loop is running and attempt
        # to schedule the execute_async method there. If no loop is found or the loop is not
        # running, asyncio.run can be run instead.
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return loop.run_until_complete(
                self.execute_async(access_token, query, max_tries, **kwargs)
            )

        return asyncio.run(self.execute_async(access_token, query, max_tries, **kwargs))

    async def execute_async(
        self, access_token: str, query: str, max_tries: int = 1, **kwargs
    ):
        """Coroutine for executing a GraphQL query to the Tibber API asynchronously.

        :param access_token: The Tibber API token to use for the request.
        :param query: The query to send to the Tibber API.
        :param max_tries: The amount of attempts before giving up. Set to None for infinite tries.
        :param **kwargs: Arguments to be passed in to the backoff.on_exception decorator
        """
        backoff_execution = backoff.on_exception(
            backoff.expo,
            [
                gql.transport.exceptions.TransportClosed,
                websockets.exceptions.ConnectionClosedError,
            ],
            max_tries=max_tries,
            max_time=100,
            jitter=backoff.full_jitter,
            on_success=self._success_handler,
            on_backoff=self._backoff_handler,
            on_giveup=self._giveup_handler,
            **kwargs,
        )(self.execute_async_single)

        result = await backoff_execution(access_token, query)
        return result

    async def execute_async_single(self, access_token: str, query: str):
        try:
            result = await self.gql_client.execute_async(gql.gql(query))
        except TransportQueryError as e:
            for error in e.errors:
                self._process_error(error)
        except asyncio.exceptions.TimeoutError:
            _logger.error(
                "Timed out when executing a query. Check your connection to the Tibber API or the Tibber API status."
            )
            _logger.debug("query information:\n" + query)
            raise APIException("Timed out when executing query.")
        return result

    def _process_error(self, error):
        try:
            code = error["extensions"]["code"]
            message = error["message"]
        except KeyError:
            raise APIException(error)

        if code == "UNAUTHENTICATED":
            raise UnauthenticatedException(message)

        raise APIException(error)

    def _success_handler(self, details): ...

    def _backoff_handler(self, details):
        _logger.warning(
            "Backing off after {tries} tries. Calling {target} in {wait:.1f} seconds.".format(
                **details
            )
        )

    def _giveup_handler(self, details):
        _logger.error(
            "Gave up running {target} after {tries} tries. {elapsed:.1f} seconds have passed.".format(
                **details
            )
        )
