# finpipe — architecture (v2)

END GOAL (import style) for easy access in other projects:

```python
import finpipe as fp

fp.fundamentals.filings  # submodules as attributes on the package 
#fp.techncicals.ohlcv
#...

# or explicit imports:
from finpipe import fundamentals
from finpipe.fundamentals import filings
```

`from fp import fp.fundamentals` is not valid: after `import finpipe as fp`, `fp` is the package module; use `fp.fundamentals` or `from finpipe import fundamentals`, not `from fp import …` with a dotted name on the right.



High-level design: **shared engine in `core`**, **pluggable providers**, **central fallback chains**, **thin domain APIs** (`technicals`, `fundamentals`, …). Naming conventions are in [`rules.md`](rules.md).

## Layers

```text
┌─────────────────────────────────────────────────────────────┐
│  Domain modules (technicals, fundamentals, macro, …)         │
│  Thin public APIs: getXxx(ticker, …)                         │
└───────────────────────────┬───────────────────────────────────┘
                            │ uses
┌───────────────────────────▼───────────────────────────────────┐
│  core                                                         │
│  • chains   — registry of provider order per (chain_key, asset)│
│  • fallback — try providers in order                          │
│  • result / exceptions — FinPipeResult, ProviderError, …      │
│  • rate_limiter — JSON-backed + deque                         │
│  • config — ~/.finpipe/config.yml                             │
│  • cache — local parquet/json                                 │
│  • utils — normalize_ticker, dates, …                         │
└───────────────────────────┬───────────────────────────────────┘
                            │ calls
┌───────────────────────────▼───────────────────────────────────┐
│  providers                                                    │
│  One adapter per vendor (yfinance_adapter, finnhub_adapter, …) │
└───────────────────────────────────────────────────────────────┘
```

Domain code **does not** embed long “try A then B” lists. It asks **`core`** for a chain and runs the fallback engine.

## Fallback and chains

- **`chains.py`**: single place where **every** `FallbackChain` is defined (per PDF: ohlcv, statements, filings, … with **EQUITY / CRYPTO / ANY**).
- **`fallback.py`**: engine only — **no** chain definitions inside (v2).
- Domain modules call something like **`getChain(chainKey, ticker)`** (exact name TBD in code) and never instantiate ad-hoc chains.

**Asset class** (from PDF): treat ticker as **CRYPTO** if it looks like `…/…`, `-PERP`, `-USDT`, etc.; otherwise **EQUITY**. **ANY** means both.

## User data on disk (`~/.finpipe/`)

| Path | Purpose |
|------|---------|
| `config.yml` | API keys and settings |
| `rate_limits.json` | Rate limiter state (v2; replaces old SQLite `rate_limits.db`) |

Optional cache subtrees (per PDF): `cache/`, `technicals/`, `fundamentals/`, … — created on first run.

## Provider order (examples from v2 PDF)

Illustrative only; **source of truth** should be `core/chains.py` once implemented.

- **ohlcv EQUITY:** yfinance → finnhub → alpha_vantage → polygon  
- **ohlcv CRYPTO:** ccxt → tardis → coingecko  
- **statements EQUITY:** yfinance → simfinapi → fmpsdk → alpha_vantage → sec_edgar  
- **filings EQUITY:** sec_edgar → sec_downloader → fmpsdk  

## Build / dependency direction

Intended build order (from PDF):

`core` → `technicals` → `fundamentals` → `macro` → `derivatives` → `sentiment`

Lower layers must not import higher layers.

## Displays

**`finpipe.displays`** holds formatting (e.g. Rich, tables). It may call domain or third-party helpers for demos, but **production pipelines** should keep business logic in `core` + domain modules, not in display code.

## SEC / Edgar

Tools like **EdgarTools** are **separate** from the core fallback story: they are one way to hit SEC data (often used from `displays` or a dedicated adapter), and must respect SEC identity + fair-access limits. See project docs and SEC guidance when scaling requests.
