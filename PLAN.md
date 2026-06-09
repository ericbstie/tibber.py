# tibber.py — Simplification & Robustness Plan

## Project intent (as understood)

tibber.py is an unofficial, **beginner-friendly** Python wrapper for Tibber's GraphQL API.
Its design goals, which this plan preserves:

- **1:1 mirroring** of the Tibber GraphQL types as Python classes (`tibber.types.*`), each
  wrapping a cached response dict with snake_case properties, plus convenience shortcuts
  (e.g. `home.address1`).
- **Synchronous-first ergonomics** (`account = tibber.Account(token)`) on top of the async
  `gql` library, with async variants available.
- **Live measurements** over websockets with an event-decorator callback API
  (`@home.event("live_measurement")`).

## Constraints (decided)

- **Strictly backwards compatible.** No public API changes, Python floor stays at **3.9**.
  Only fixes to code that *already crashes* are allowed (it can't break anyone).
- **python-semantic-release** for automated changelog + version bump + publish.
- **Tests run offline by default**; live demo-API tests become opt-in.

## Current pain points

| Area | Problem |
|---|---|
| Packaging | Legacy `setup.py`, no `pyproject.toml`, no lockfile; deps duplicated and version-mismatched between `setup.py` (`gql==3.5.3`) and three CI workflows (`gql==3.5.2`). |
| Onboarding | No documented dev setup; contributors must guess the pip incantation from CI yaml. |
| Lint/types | flake8 + black only, line-length configs disagree (160 vs 88), **no type checking**; annotations are wrong in places (`user_agent: str = None`), mutable default args. |
| Tests | Every run hits the live demo API and **silently falls back** to canned JSON — flaky and non-deterministic. Realtime tests need a real websocket. Query-building logic and error mapping are untested. |
| CI | Three overlapping workflows install dependencies by hand, in different versions. |
| Releases | Manual version-bump commits, manual GitHub release, deprecated `setup.py sdist bdist_wheel` build, PyPI long-lived token, **no changelog**. |
| Latent bugs | `Account.token` setter crashes on its own error path (`"..." + type(token)`); `result` can be unbound in `QueryExecutor.execute_async_single`; `QueryBuilder.single_home` is a malformed classmethod; `loop.run_until_complete()` on an already-running loop always raises. |

## Phase 1 — Packaging & tooling foundation (uv)

1. Add **`pyproject.toml`** (PEP 621, `hatchling` backend), migrate all metadata from
   `setup.py`, then delete `setup.py`.
   - Single dependency list: `gql[aiohttp,websockets]>=3.5,<4`, `graphql-core>=3.2.3`,
     `backoff>=2.2.1`, `asyncio-atexit>=1.0.1`. (Resolves the 3.5.2/3.5.3 mismatch.)
   - `requires-python = ">=3.9"`.
   - Version stays single-sourced in `tibber/__init__.py` (`tool.hatch.version.path`),
     so `tibber.__version__` keeps working and semantic-release can bump it.
2. Adopt **uv**: commit `uv.lock`; add a `dev` dependency group (pytest, pytest-cov,
   pytest-timeout, ruff, ty) and a `docs` group (sphinx deps, replacing
   `docs/requirements.txt`).
3. Add **CONTRIBUTING.md** + README "Development" section: `uv sync`, `uv run pytest`,
   `uv run ruff check`, `uv run ty check`. Getting started becomes two commands.

## Phase 2 — Lint, format, type-check (ruff + ty)

1. **ruff** replaces black + flake8 + the ad-hoc isort comments:
   - `ruff format` (black-compatible, line length 88 — the code is already black-formatted).
   - `ruff check` with `E, F, W, I, UP, B, SIM, C4, RUF`, `target-version = "py39"`,
     per-file ignore `tibber/__init__.py: E402` (intentional import order).
   - Delete `.flake8`.
2. **ty** as the type checker over `tibber/`. To get it green *without* behavior change:
   - Correct annotations (`Optional[str]` where `None` defaults exist, return types on the
     ~30 type-class properties, `dict`/`list` parametrization).
   - Replace mutable default args (`transport_kwargs={}` → `None` + fill-in inside) —
     signature-compatible.
   - ty is young; if a rule misfires we suppress per-line rather than contort the code.
3. Optional **pre-commit** config running `ruff check --fix` + `ruff format`.

## Phase 3 — Robust, deterministic tests

1. **Offline by default**: the `account` fixture loads recorded demo data
   (`tests/backup_demo_data.json`, refreshed and renamed to `tests/fixtures/demo_account.json`)
   with `immediate_update=False` and a stubbed transport, so no test opens a connection
   unless explicitly marked. Delete the silent try/except fallback in `conftest.py`.
2. **Markers** (`strict-markers` on): `live` for demo-API queries, `realtime` for websocket
   tests. Default `addopts = -m "not live and not realtime"`.
3. **New unit tests** for the currently untested core:
   - Golden-output tests for every `QueryBuilder` query method (these lock current behavior
     before any internal cleanup).
   - `combine_dicts` edge cases.
   - Error mapping: `UNAUTHENTICATED` → `UnauthenticatedException`, unknown → `APIException`.
   - Retry/backoff paths with a mocked transport.
4. Move coverage config into `pyproject.toml`, add a `fail_under` floor at the current
   level and ratchet it up as coverage grows.

## Phase 4 — CI consolidation

1. Replace `pytests.yml`, `code-coverage.yml`, `code-formatting.yml` with one **`ci.yml`**:
   - `lint`: `ruff check` + `ruff format --check`
   - `typecheck`: `ty check`
   - `test`: matrix over Python 3.9 / 3.11 / 3.13 using `astral-sh/setup-uv` (built-in
     dependency caching); coverage uploaded from one matrix entry via the codecov action.
2. New **`live.yml`**: weekly cron + manual dispatch, runs `-m "live or realtime"` against
   the demo API to catch upstream API drift without blocking PRs.
3. Add a conventional-commit check on PR titles (`amannn/action-semantic-pull-request`)
   so semantic-release always has parseable input.
4. Keep `codeql-analysis.yml` as is.

## Phase 5 — Release automation (python-semantic-release)

1. Configure `[tool.semantic_release]` in `pyproject.toml`:
   - `version_variables = ["tibber/__init__.py:__version__"]`
   - Conventional-commit parser: `fix:` → patch, `feat:` → minor, `BREAKING CHANGE` → major.
   - Generates/maintains **CHANGELOG.md** and GitHub Releases.
2. New **`release.yml`** replacing `publish-to-pypi.yml`: on push to `master` →
   semantic-release (bump + changelog + tag + GitHub release) → `uv build` →
   publish via **PyPI Trusted Publishing** (OIDC). The long-lived `PYPI_API_TOKEN`
   secret is removed. *(One-time manual step: enable the trusted publisher on PyPI.)*
3. Backfill an initial CHANGELOG.md from existing git history; manual
   `chore: bump version` commits are retired.

## Phase 6 — Safe internal cleanups (strictly non-breaking)

Only after Phase 3's golden tests are in place:

1. Fix the four latent crashes listed above (token-setter concat, unbound `result`,
   `single_home`, the running-loop branch — replace the latter with a clear error message
   pointing users to `update_async()`, since it can only ever raise today).
2. Make `_process_error` handle multiple GraphQL errors instead of raising on the first
   iteration of a loop (same exception types raised).
3. Deduplicate the four copies of pagination-argument building in `QueryBuilder`
   (`consumption_query`, `production_query`, `range_query`, `price_info_range_query`) into
   one helper — golden tests guarantee identical query strings.
4. Lazy `%`-style logging instead of string concatenation in log calls.

Explicitly **out of scope** (would be breaking or risky): redesigning the sync-over-async
facade, dataclass-based types, GraphQL-variable-based queries, dropping Python 3.9,
renaming `NonDecoratedTibberHome`.

## Suggested order of execution

Each phase is one PR-sized unit with conventional commits:

1. Phase 1 (packaging/uv) — everything else builds on it.
2. Phase 2 (ruff/ty) — small diff, removes two CI workflows' tooling.
3. Phase 3 (tests) — must land before Phase 6 touches internals.
4. Phase 4 (CI) — wires Phases 1–3 together.
5. Phase 5 (semantic-release) — independent, needs the PyPI trusted-publisher setup.
6. Phase 6 (cleanups) — protected by Phase 3's golden tests.
