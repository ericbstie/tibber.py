import asyncio
import atexit
import logging
import threading

import backoff
import gql
import websockets
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

from tibber import API_ENDPOINT
from tibber.exceptions import APIException, UnauthenticatedException

_logger = logging.getLogger(__name__)


class QueryExecutor:
    """A class for executing queries.

    The async core runs on a dedicated event loop in a background thread.
    The sync methods are a thin facade that submit work to that loop, so
    they are safe to call from any context - including inside a running
    event loop.
    """

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

        self._loop = asyncio.new_event_loop()
        self._loop_thread = threading.Thread(
            target=self._loop.run_forever, name="tibber-query-executor", daemon=True
        )
        self._loop_thread.start()
        atexit.register(self._shutdown)

        self._run_coroutine_threadsafe(self.__ainit__(session))

    async def __ainit__(self, session):
        self.session = session or await self.gql_client.connect_async()

    def _run_coroutine_threadsafe(self, coroutine):
        """Runs a coroutine on the executor's event loop and waits for the result."""
        return asyncio.run_coroutine_threadsafe(coroutine, self._loop).result()

    def _shutdown(self):
        if self._loop.is_closed():
            return
        try:
            self._run_coroutine_threadsafe(self.gql_client.close_async())
        finally:
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._loop_thread.join(timeout=5)
            self._loop.close()

    def execute_query(
        self, access_token: str, query: str, max_tries: int = 1, **kwargs
    ):
        """Executes a GraphQL query to the Tibber API.

        :param access_token: The Tibber API token to use for the request.
        :param query: The query to send to the Tibber API.
        :param max_tries: The amount of attempts before giving up. Set to None for infinite tries.
        :param **kwargs: Arguments to be passed in to the backoff.on_exception decorator
        """
        return self._run_coroutine_threadsafe(
            self._execute_with_backoff(access_token, query, max_tries, **kwargs)
        )

    async def execute_async(
        self, access_token: str, query: str, max_tries: int = 1, **kwargs
    ):
        """Coroutine for executing a GraphQL query to the Tibber API asynchronously.

        :param access_token: The Tibber API token to use for the request.
        :param query: The query to send to the Tibber API.
        :param max_tries: The amount of attempts before giving up. Set to None for infinite tries.
        :param **kwargs: Arguments to be passed in to the backoff.on_exception decorator
        """
        future = asyncio.run_coroutine_threadsafe(
            self._execute_with_backoff(access_token, query, max_tries, **kwargs),
            self._loop,
        )
        return await asyncio.wrap_future(future)

    async def _execute_with_backoff(
        self, access_token: str, query: str, max_tries: int = 1, **kwargs
    ):
        backoff_execution = backoff.on_exception(
            backoff.expo,
            (
                gql.transport.exceptions.TransportClosed,
                websockets.exceptions.ConnectionClosedError,
            ),
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
            result = await self.session.execute(gql.gql(query))
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
