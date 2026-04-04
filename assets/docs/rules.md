# finpipe — project rules

Conventions for this repository. **Flow, pipelines, and fallback design** live in [`architecture.md`](architecture.md).

## Naming

| Kind | Style | Examples |
|------|--------|----------|
| **Functions** | `camelCase`; prefer a `get` prefix for fetchers | `getFilings`, `getOhlcv`, `getChain` |
| **Classes** | `PascalCase` | `FinPipeResult`, `FallbackChain`, `ProviderError` |
| **Variables** (general) | `snake_case` | `ticker`, `start_date`, `just_a_var` |
| **Constants** | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT`, `MAX_RETRIES` |
| **Modules / packages** | `snake_case` (PEP 420 / import paths) | `financial_statements`, `ohlcv_historical`, `sec_edgar_adapter` |

Notes:

- Python’s stdlib style guide (PEP 8) defaults to `snake_case` for functions; this project **opts into `camelCase` for public functions** so names read consistently with the “`getXxx`” pattern. Keep **private helpers** as `_snake_case` if you want to avoid mixing styles inside a file.
- **Constants** are module-level names that are not meant to be reassigned (not enforced by the language).

## Package layout

- **Top-level domains** are **broad categories**: `fundamentals`, `technicals`, `core`, `providers`, `displays`, etc.
- **Submodules** split by **feature / dataset**, similar to common libraries (e.g. EdgarTools-style `financials.*` → our `fundamentals.financials.income`, `fundamentals.financials.balance`, …).
- **Providers** stay isolated under `finpipe.providers` (one adapter per vendor / integration).
- **Rendering / printing** (Rich, tables) is implemented under `finpipe.displays` but **users should not import `displays` by default** — use `fundamentals.show(ticker, section=…)` (dispatch), `fundamentals.showOverview(ticker)` (what’s available), `fundamentals.financials.show(ticker, kind)`, or per-file `show` on each fundamentals submodule (e.g. `earnings.show`, `financials.income.show`). `StatementKind` is re-exported from `fundamentals.financials`.

## Imports (public API)

Prefer stable paths users can rely on:

```text
finpipe.fundamentals.financials.income
finpipe.fundamentals.filings
finpipe.technicals.ohlcv_historical
finpipe.core.chains
```

`finpipe.displays` exists for shared render code and tests; normal apps import **fundamentals / technicals** and call `show*` or `get*` there.

Add deeper nesting only when a category naturally splits (e.g. `fundamentals.filings.sec` later), not for one-off helpers.

## Docs

- **`rules.md`** (this file): naming + layout conventions.
- **`architecture.md`**: data flow, hierarchy, fallback chains, and how layers connect.
