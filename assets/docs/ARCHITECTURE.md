# finpipe — architecture (v2)

END GOAL (import style) for easy access in other projects:

```python
import finpipe as fp

fp.technicals.fetchOhlcv("NVDA").print()
fp.fundamentals.showFinancials("NVDA", "income")

# or explicit imports:
from finpipe import fundamentals
from finpipe.fundamentals import showFinancials
```

`from fp import fp.fundamentals` is not valid: after `import finpipe as fp`, `fp` is the package module; use `fp.fundamentals` or `from finpipe import fundamentals`, not `from fp import …` with a dotted name on the right.



High-level design: **shared engine in `core`**, **pluggable providers**, **central fallback chains**, and compact domain packages. Domain packages keep public functions in a module-named file (`technicals.py`, `fundamentals.py`), data objects in `objects.py`, private shared helpers in `helpers.py`, and re-export public functions from `__init__.py`. Naming conventions are in [`RULES.md`](RULES.md).

## Layers

```text
┌─────────────────────────────────────────────────────────────┐
│  Domain packages (technicals, fundamentals, macro, …)        │
│  <domain>.py · objects.py · helpers.py                        │
└───────────────────────────┬───────────────────────────────────┘
                            │ uses
┌───────────────────────────▼───────────────────────────────────┐
│  core                                                         │
│  core.py — provider chain registry and fallback runner        │
│  objects.py — chain and error classes                         │
│  helpers.py — private shared helpers                           │
└───────────────────────────┬───────────────────────────────────┘
                            │ calls
┌───────────────────────────▼───────────────────────────────────┐
│  providers                                                    │
│  one module per vendor; helpers.py — shared normalization      │
└───────────────────────────────────────────────────────────────┘
```

Domain code **does not** embed long “try A then B” lists. It asks **`core`** for a chain and runs the fallback engine.

Implemented first slice: `finpipe.technicals.fetchOhlcv()` resolves the OHLCV
chain, invokes provider adapters, and returns `OhlcvData`. The object carries
normalized bars plus provider/fallback provenance and supports `.print()` and
`.toDataFrame()`. The initial chain currently registers yfinance only; add a
provider to `core/core.py` after implementing its function and normalization.

## Fallback and chains

- **`core/core.py`**: single place where provider order is registered and fallback is run.
- **`core/objects.py`**: `FallbackChain` and provider/fallback error classes.
- Domain functions call **`getChain(chainKey, ticker)`** and never instantiate ad-hoc chains.

**Asset class** (from PDF): treat ticker as **CRYPTO** if it looks like `…/…`, `-PERP`, `-USDT`, etc.; otherwise **EQUITY**. **ANY** means both.

## User data on disk (`~/.finpipe/`)

| Path | Purpose |
|------|---------|
| `config.yml` | API keys and settings |
| `rate_limits.json` | Rate limiter state (v2; replaces old SQLite `rate_limits.db`) |

Cache, configuration, and rate-limiter modules remain planned; they are not implemented in this version.

## Provider order (examples from v2 PDF)

Illustrative only; the current source of truth is `core/core.py`.

- **ohlcv EQUITY:** yfinance → finnhub → alpha_vantage → polygon  
- **ohlcv CRYPTO:** ccxt → tardis → coingecko  
- **statements EQUITY:** yfinance → simfinapi → fmpsdk → alpha_vantage → sec_edgar  
- **filings EQUITY:** sec_edgar → sec_downloader → fmpsdk  

## Build / dependency direction

Intended build order (from PDF):

`core` → `technicals` → `fundamentals` → `macro` → `derivatives` → `sentiment`

Lower layers must not import higher layers.

## Displays

**`finpipe.displays.displays`** holds formatting (e.g. Rich, tables). It may call provider objects for rendering, while data retrieval and fallback remain in core and domain modules.

## SEC / Edgar

Tools like **EdgarTools** are **separate** from the core fallback story: they are one way to hit SEC data (often used from `displays` or a dedicated adapter), and must respect SEC identity + fair-access limits. See project docs and SEC guidance when scaling requests.
