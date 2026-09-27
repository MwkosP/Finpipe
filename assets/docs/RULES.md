# finpipe — project rules

Conventions for this repository. **Flow, pipelines, and fallback design** live in [`architecture.md`](architecture.md).

## Naming

| Kind | Style | Examples |
|------|--------|----------|
| **Functions** | `camelCase`; prefer a `get` prefix for fetchers | `getFilings`, `getOhlcv`, `getChain` |
| **Classes** | `PascalCase` | `FinPipeResult`, `FallbackChain`, `ProviderError` |
| **Variables** (general) | `snake_case` | `ticker`, `start_date`, `just_a_var` |
| **Constants** | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT`, `MAX_RETRIES` |
| **Modules / packages** | `snake_case` (PEP 420 / import paths) | `technicals`, `fundamentals`, `providers` |

Notes:

- Python’s stdlib style guide (PEP 8) defaults to `snake_case` for functions; this project **opts into `camelCase` for public functions** so names read consistently with the “`getXxx`” pattern. Keep **private helpers** as `_snake_case` if you want to avoid mixing styles inside a file.
- **Constants** are module-level names that are not meant to be reassigned (not enforced by the language).
- Package-level `helpers.py` modules hold shared implementation details. Keep helper functions private (leading `_`); public functions and classes belong in their feature/API modules.

## Package layout

- **Top-level domains** are **broad categories**: `fundamentals`, `technicals`, `core`, `providers`, `displays`, etc.
- **Domain packages** collect public functions in a module-named file (for example, `technicals/technicals.py`), data classes and shared type aliases in `objects.py`, and private shared functions in `helpers.py`.
- **Providers** stay isolated under `finpipe.providers`, with one module per vendor (for example, `yfinance.py`, `sec_edgar.py`).
- **Rendering / printing** (Rich, tables) is implemented under `finpipe.displays`; callers use public functions re-exported from their domain package.

## Imports (public API)

Prefer stable paths users can rely on:

```text
finpipe.fundamentals.showFinancials
finpipe.technicals.fetchOhlcv
finpipe.core.getChain
```

`finpipe.displays` contains shared render code; normal apps import **fundamentals / technicals** and call functions re-exported by those packages.

Keep domain APIs together in the module-named file; private implementation helpers stay in `helpers.py`.

## Docs

- **`rules.md`** (this file): naming + layout conventions.
- **`architecture.md`**: data flow, hierarchy, fallback chains, and how layers connect.
