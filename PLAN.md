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

## Surrounding context (PRs, issues, branches)

### PR #67 — "Use `uv` and `ruff` instead of `setup.py`, `flake8` and `black`" (open, CI green)

The owner's open PR (branch `refactor/uv`, mergeable, all 20 checks passing) already
delivers a large part of the original Phase 1/2/4 scope:

- `pyproject.toml` (uv_build backend), **src layout** (`src/tibber/`), `uv.lock`,
  dev group (pytest, pytest-cov, ruff), `.python-version` (3.14).
- ruff replaces black + flake8; one consolidated `code-quality.yml` (ruff, pytest matrix
  3.9/3.11/3.13/3.14, coverage, build + wheel/sdist smoke tests).
- `release.yml` already publishes with `uv build` + `uv publish` via **PyPI Trusted
  Publishing** (OIDC) on GitHub release.

**Decision: this plan builds on PR #67 instead of duplicating it.** Merge #67 first
(or rebase this work onto `refactor/uv`). Gaps in #67 to fix on top:

1. **CodeQL workflow was deleted** in #67 — likely unintentional; restore it (or confirm
   removal was deliberate).
2. CI runs `ruff check` but **not `ruff format --check`** — formatting is unenforced.
3. `E402` is ignored **globally**; should be a per-file ignore for `tibber/__init__.py`
   only, and the lint rule set should be expanded (`I`, `UP`, `B`, `SIM`, `C4`, `RUF`).
4. Version is now duplicated (`pyproject.toml` + `src/tibber/__init__.py`) — fine once
   semantic-release bumps both (`version_toml` + `version_variables`).
5. `pytest-timeout` is used by realtime tests but missing from the dev group.
6. README badges still point at the old `BeatsuDev/tibber.py` repo paths.
7. Tests/conftest unchanged — still live-API with silent fallback (Phase 3 below).

### Open issues this plan addresses

| Issue | What it reports | Where it lands |
|---|---|---|
| **#65** `fetch_price_info` fails in async contexts (bug) | `loop.run_until_complete()` on a running loop always raises `RuntimeError`. Owner: "needs deeper refactoring." | Phase 6.1 — a strictly-compatible fix exists: when a loop is already running, execute the coroutine in a dedicated worker thread with its own loop and block on the result. Sync API keeps working inside async code. Regression test from the issue's snippet. |
| **#35** Live feed stops reconnecting after ~a day | Logs show `TypeError: catching classes that do not inherit from BaseException is not allowed` — caused by passing a **list** instead of a tuple of exception types to `backoff.on_exception` (in `query_executor.py` and `home.py`). The retry wrapper itself crashes, so reconnects die. | Phase 6.2 — list → tuple, plus a test that the backoff wrappers actually catch the intended exceptions. Full teardown-and-reconnect hardening noted as follow-up. |
| **#48** "Mock data for tests" (owner) | Hardcoded demo-account values break when the demo account changes; wants mocked API data. | Phase 3 — exactly the offline-by-default fixture strategy. |

Out of scope (feature requests, kept open): #44 event enums, #36 datetime `before`/`after`
arguments, #26 multi-home live feeds. Phase 3's test scaffolding and Phase 6's loop
handling make all three easier later.

### Branches / releases

No stale branches: only `master`, `refactor/uv` (PR #67) and this plan branch. Releases
v0.1.0–v0.7.1 are manual GitHub releases with hand-written notes — confirms the need for
Phase 5.

## Current pain points (on master)

| Area | Problem |
|---|---|
| Packaging | Legacy `setup.py`, deps duplicated and version-mismatched vs CI (`gql==3.5.3` vs `3.5.2`). → *solved by PR #67* |
| Onboarding | No documented dev setup. → *mostly solved by #67 (uv), CONTRIBUTING.md still missing* |
| Lint/types | No type checking; wrong annotations (`user_agent: str = None`), mutable default args. → *ruff lands in #67; ty and annotation fixes remain* |
| Tests | Live demo API with **silent fallback** to canned JSON; query building and error mapping untested. (Issue #48) |
| Releases | Manual version bumps and hand-written release notes; no changelog file. → *#67 adds Trusted Publishing; automation remains* |
| Latent bugs | Running-loop branch always raises (#65); backoff exception **lists** break retries (#35); `Account.token` setter crashes on its own error path; `result` can be unbound in `execute_async_single`; `QueryBuilder.single_home` is a malformed classmethod. |

## Phase 1 — Land PR #67, then close its gaps

1. Merge PR #67 (owner's call) and rebase this branch onto it.
2. Restore `codeql-analysis.yml` (or get explicit sign-off on removing it).
3. Add `ruff format --check` to CI; expand ruff rules (`E, F, W, I, UP, B, SIM, C4, RUF`),
   `target-version = "py39"`, per-file `E402` ignore for `tibber/__init__.py`.
4. Add `pytest-timeout` to the dev group; fix the stale `BeatsuDev` badge URLs.
5. Add **CONTRIBUTING.md** + README "Development" section: `uv sync`, `uv run pytest`,
   `uv run ruff check`, `uv run ty check`.

## Phase 2 — Type checking (ty)

1. Add **ty** to the dev group and CI over `src/tibber/`. To get it green *without*
   behavior change:
   - Correct annotations (`Optional[str]` where `None` defaults exist, return types on the
     ~30 type-class properties, `dict`/`list` parametrization).
   - Replace mutable default args (`transport_kwargs={}` → `None` + fill-in inside) —
     signature-compatible.
   - ty is young; suppress per-line where it misfires rather than contort code.

## Phase 3 — Robust, deterministic tests (closes #48)

1. **Offline by default**: the `account` fixture loads recorded demo data
   (`tests/backup_demo_data.json`, refreshed and renamed `tests/fixtures/demo_account.json`)
   with `immediate_update=False` and a stubbed transport. Delete the silent try/except
   fallback in `conftest.py`.
2. **Markers** (`strict-markers`): `live` for demo-API queries, `realtime` for websocket
   tests; default `addopts = -m "not live and not realtime"`.
3. **New unit tests** for the untested core:
   - Golden-output tests for every `QueryBuilder` method (locks behavior before Phase 6).
   - `combine_dicts` edge cases; error mapping (`UNAUTHENTICATED` →
     `UnauthenticatedException`); retry/backoff paths with a mocked transport.
4. Coverage config into `pyproject.toml` with a `fail_under` floor, ratcheted up over time.
5. New **`live.yml`** workflow: weekly cron + manual dispatch runs `-m "live or realtime"`
   against the demo API to catch upstream drift without blocking PRs.

## Phase 4 — Release automation (python-semantic-release)

1. `[tool.semantic_release]` in `pyproject.toml`:
   - `version_toml = ["pyproject.toml:project.version"]` and
     `version_variables = ["src/tibber/__init__.py:__version__"]` (keeps both in sync).
   - Conventional-commit parser: `fix:` → patch, `feat:` → minor, `BREAKING CHANGE` → major.
   - Maintains **CHANGELOG.md** + GitHub Releases.
2. Extend #67's `release.yml`: on push to `master` → semantic-release (bump + changelog +
   tag + GitHub release) → existing `uv build` + Trusted Publishing steps. Manual
   `chore: bump version` commits retire.
3. Conventional-commit check on PR titles (`amannn/action-semantic-pull-request`).
4. Backfill an initial CHANGELOG.md from the existing release notes.

## Phase 5 — Safe internal cleanups (strictly non-breaking)

Only after Phase 3's golden tests are in place:

1. **Fix #65**: replace the dead `loop.run_until_complete` branch in
   `QueryExecutor.execute_query` (and `start_live_feed`) with a worker-thread execution
   path, so sync calls work from async contexts. Regression test from the issue.
2. **Fix #35's TypeError**: backoff exception lists → tuples in `query_executor.py` and
   `home.py`; test the retry wrappers.
3. Fix the remaining latent crashes: token-setter string concat, unbound `result` in
   `execute_async_single`, malformed `QueryBuilder.single_home`.
4. `_process_error`: handle multiple GraphQL errors (same exception types raised).
5. Deduplicate the four copies of pagination-argument building in `QueryBuilder`
   (golden tests guarantee identical query strings).
6. Lazy `%`-style logging instead of string concatenation in log calls.

Explicitly **out of scope** (would be breaking or risky): redesigning the sync-over-async
facade, dataclass-based types, GraphQL-variable-based queries, dropping Python 3.9,
renaming `NonDecoratedTibberHome`.

## Suggested order of execution

1. Phase 1 — gated on merging PR #67; everything rebases onto it.
2. Phase 2 (ty) — small diff.
3. Phase 3 (tests) — must land before Phase 5 touches internals; closes #48.
4. Phase 4 (semantic-release) — independent; needs the PyPI trusted publisher #67 set up.
5. Phase 5 (cleanups) — protected by Phase 3's golden tests; closes #65, fixes #35's
   immediate crash.
