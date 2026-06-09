# Contributing to tibber.py

Thank you for considering contributing! Issues, discussions and pull requests are all
welcome — see [this overview](https://github.com/ericbstie/tibber.py/discussions/46) for
where to post what.

## Development setup

tibber.py uses [uv](https://docs.astral.sh/uv/) for everything: environments,
dependencies, running tools and building the package.

```bash
git clone https://github.com/ericbstie/tibber.py
cd tibber.py
uv sync          # creates .venv and installs all (dev) dependencies
```

That's it. Run things with `uv run`:

```bash
uv run pytest              # run the test suite
uv run ruff check src      # lint
uv run ruff format         # format
```

## Code style

Formatting and linting are enforced by [ruff](https://docs.astral.sh/ruff/) in CI;
configuration lives in `pyproject.toml`. Before pushing:

```bash
uv run ruff format
uv run ruff check src --fix
```

## Tests

```bash
uv run pytest tests
```

The test suite talks to the Tibber demo API using the public demo token, so no
credentials are needed. When adding features, please add tests — pure logic (query
building, error mapping) should be testable without network access.

## Pull requests

Keep each pull request focused on one specific change so it can be reviewed and merged
independently.

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):

- `fix: ...` — bug fixes
- `feat: ...` — new features
- `feat!: ...` or a `BREAKING CHANGE:` footer — breaking changes
- `docs: ...`, `test: ...`, `ci: ...`, `refactor: ...`, `chore: ...` — everything else
