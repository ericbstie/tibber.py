# CHANGELOG

Releases from v0.8.0 onward are generated automatically by
[release-please](https://github.com/googleapis/release-please) from
[conventional commit](https://www.conventionalcommits.org/) messages. Earlier entries
below were backfilled from the GitHub release notes.

## v0.7.1 (2025-10-18)

- Added `Subscription.fetch_price_info()` for today's and tomorrow's prices at `HOURLY`
  or `QUARTER_HOURLY` resolution
- Fixed the return type of `fetch_price_info_range()` (returns a
  `SubscriptionPriceConnection`, not a `PriceInfo`)

## v0.7.0 (2025-10-13)

- Added `Subscription.fetch_price_info_range()` for historical price info at
  `QUARTER_HOURLY`, `HOURLY` or `DAILY` resolution

## v0.6.0 (2025-04-30)

- **BREAKING:** SSL connections are now verified by default. Transport options can be
  passed with `tibber.Account(token, transport_kwargs={...})`

## v0.5.0 (2025-01-06)

- Support for older Python versions
- Ability to search for price info in historical data
- Fixed a method name typo

## v0.4.0 (2023-01-20)

- Callback functions are now asynchronous (use `async def`)
- Dev: black/flake8/isort formatting; faster tests via a session-scoped account fixture

## v0.3.0 (2023-01-05)

- Improved realtime websocket connection handling (fewer "Connection limit reached" errors)
- `start_live_feed()` now checks that realtime consumption is enabled before connecting
- Added `Account.update()` as an alias for `fetch_all()`
- Better websocket logging; `QueryExecutor` now reuses a permanent session

## v0.2.1 (2022-12-01)

- Added exit conditions for live feeds:
  `home.start_live_feed(exit_condition=lambda data: data.power > 1000)`
- Fixed duplicate callback invocations when restarting a live feed

## v0.2.0 (2022-11-29)

- Realtime data now uses the `graphql-transport-ws` subprotocol via `gql`
- **BREAKING:** `home.start_livefeed()` renamed to `home.start_live_feed()`

## v0.1.1 (2022-09-28)

- Updated the demo token

## v0.1.0 (2022-08-01)

- **BREAKING:** `tibber.Client` renamed to `tibber.Account`
- Historical data support
- More documentation (https://tibberpy.readthedocs.io) and test coverage
