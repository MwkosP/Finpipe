# Finpipe Architecture

## Problem

Financial data sources are unreliable. Every provider has some combination of rate limits, API key tiers, cost walls, or random outages. Writing "try yfinance, if it fails try Finnhub, if that fails..." logic in every script is fragile and unmaintainable. Finpipe solves this at the engine level so modules never think about it.

---

## Directory Structure

```
finpipe/
+-- ARCHITECTURE.md          <- this file
+-- PROVIDERS.md             <- provider reference (keys, limits, tiers)
+-- README.md
+-- cli.py                   <- CLI entry point (finpipe status, finpipe fetch, etc.)
+-- main.py
+-- pyproject.toml
+-- docs/
|   +-- quickstart.md
|   +-- modules/
|       +-- technicals.md
|       +-- fundamentals.md
+-- examples/
|   +-- technicals_ohlcv.py
|   +-- fundamentals_statements.py
+-- tests/
|   +-- canary/              <- live smoke tests (hit real APIs)
|   +-- integration/
|   +-- unit/
+-- finpipe/
    +-- core/                <- engine layer (no external API calls)
    |   +-- result.py        <- FinPipeResult dataclass
    |   +-- exceptions.py    <- ProviderError, RateLimitError, NoDataError
    |   +-- cache.py         <- in-memory + disk cache
    |   +-- rate_limiter.py  <- JSON-backed sliding window rate limiter
    |   +-- fallback.py      <- FallbackChain execution engine
    |   +-- chains.py        <- central chain registry + asset class routing
    |   +-- config.py        <- API keys, paths, env loading
    |   +-- utils.py         <- ticker normalization, detect_asset_class
    +-- providers/           <- dumb adapters (fetch + normalize schema only)
    |   +-- yfinance_adapter.py
    |   +-- finnhub_adapter.py
    |   +-- alpha_vantage_adapter.py
    |   +-- polygon_adapter.py
    |   +-- simfinapi_adapter.py
    |   +-- fmpsdk_adapter.py
    |   +-- sec_edgar_adapter.py
    |   +-- sec_downloader_adapter.py
    |   +-- ccxt_adapter.py
    |   +-- ccxt_pro_adapter.py
    |   +-- coingecko_adapter.py
    |   +-- tardis_adapter.py
    |   +-- datareader_adapter.py
    |   +-- ib_insync_adapter.py
    +-- technicals/          <- OHLCV, orderbook, trades, volume, streaming
    +-- fundamentals/        <- statements, ratios, earnings, filings, insider, etc.
    +-- macro/               <- rates, inflation, GDP, Fama-French factors
    +-- derivatives/         <- equity options, crypto options, futures, liquidations
    +-- sentiment/           <- news, social, fear/greed, on-chain
```

---

## Layered Architecture

```
modules (technicals/, fundamentals/, ...)
    thin wrappers — own no logic, just call get_chain()
        |
        v
core/chains.py
    central registry — knows which providers serve each data type
    routes by asset class (EQUITY vs CRYPTO vs ANY)
        |
        v
core/fallback.py — FallbackChain
    owns: cache check, rate limit check, provider iteration, error collection
        |
        v
providers/
    dumb adapters — fetch from one source, normalize to standard schema, nothing else
```

**The invariant:** adding a new provider never touches module logic. Adding a new module never touches provider code. `chains.py` is the only glue between them.

---

## Core Engine

### FinPipeResult (`core/result.py`)

Every call across the entire library returns this — same shape regardless of provider:

```python
@dataclass
class FinPipeResult:
    data:       pd.DataFrame | dict | None
    source:     str        # "yfinance" | "fallback:finnhub" | "cache"
    fetched_at: datetime
    cache_hit:  bool
    warnings:   list[str]  # one entry per skipped provider, with reason
    error:      str | None # None on success
```

`source` tells you exactly who served the data. `fallback:` prefix means the primary failed. This matters for backtesting — providers disagree on adjusted prices, fiscal year definitions, etc.

### FallbackChain (`core/fallback.py`)

```
fetch(method, *args, **kwargs):
  1. Check cache → hit: return immediately with cache_hit=True
  2. For each provider in chain:
       a. Skip if rate limit exhausted (no wasted network call)
       b. Call provider.method(*args, **kwargs) via getattr
       c. Empty/None result → append warning, try next provider
       d. Success → cache result, record call, return FinPipeResult
       e. RateLimitError → mark provider exhausted, try next
       f. NoDataError / ProviderError → append warning, try next
  3. All failed → return FinPipeResult(data=None, error="All providers failed")
```

Providers are duck-typed — they just need to implement the method by name. No abstract base class required.

### Chain Registry (`core/chains.py`)

One file owns all chains. Asset class is detected from the ticker format:
- `BTC/USDT`, `ETH-PERP`, `SOL-USD` → `AssetClass.CRYPTO`
- `AAPL`, `SPY`, `MSFT` → `AssetClass.EQUITY`

```python
get_chain("ohlcv", "AAPL")      # equity chain: [yfinance, finnhub, alpha_vantage, polygon]
get_chain("ohlcv", "BTC/USDT")  # crypto chain: [ccxt, tardis, coingecko]
get_chain("statements", "AAPL") # [yfinance, simfin, fmp, alpha_vantage, sec_edgar]
get_chain("statements", "BTC")  # raises ValueError — doesn't apply to crypto
```

Every module is then a one-liner:
```python
def fetch_ohlcv(ticker, interval, start, end) -> FinPipeResult:
    return get_chain("ohlcv", ticker).fetch("ohlcv", ticker, interval, start, end)
```

### Rate Limiter (`core/rate_limiter.py`)

- **In-memory:** `deque` of UTC timestamps per provider. `_count()` is `len()`, `_trim()` is `popleft()` until cutoff. Zero I/O on reads.
- **Persistent:** JSON to `~/.finpipe/rate_limits.json` on every write. Survives restarts — your 25 Alpha Vantage calls from earlier today still count.
- **SQLite was rejected** — a disk write on every provider call is overkill for a personal tool. JSON + in-memory deque covers all needs.

```python
limiter.is_available("alpha_vantage")   # check before calling
limiter.record_call("alpha_vantage")    # call after success
limiter.mark_exhausted("polygon", retry_after=60)  # call on 429
limiter.remaining("finnhub")            # calls left in window
```

---

## Chain Registry

| Chain key         | Asset class    | Provider order (priority → fallback)                              |
|-------------------|----------------|-------------------------------------------------------------------|
| `ohlcv`           | EQUITY         | yfinance → finnhub → alpha_vantage → polygon                     |
| `ohlcv`           | CRYPTO         | ccxt → tardis → coingecko                                        |
| `orderbook`       | EQUITY         | polygon → ib_insync                                              |
| `orderbook`       | CRYPTO         | ccxt → tardis                                                    |
| `trades`          | EQUITY         | polygon → ib_insync                                              |
| `trades`          | CRYPTO         | ccxt → tardis                                                    |
| `volume`          | EQUITY         | yfinance → polygon → finnhub                                     |
| `volume`          | CRYPTO         | ccxt → coingecko                                                 |
| `statements`      | EQUITY         | yfinance → simfin → fmp → alpha_vantage → sec_edgar              |
| `ratios`          | EQUITY         | yfinance → finnhub → fmp → simfin                                |
| `earnings`        | EQUITY         | finnhub → yfinance → fmp → alpha_vantage                         |
| `insider`         | EQUITY         | finnhub → yfinance → fmp → sec_edgar                             |
| `filings`         | EQUITY         | sec_edgar → sec_downloader → fmp                                 |
| `rates`           | MACRO          | fredapi → datareader → bea                                       |
| `inflation`       | MACRO          | fredapi → bls → datareader                                       |
| `gdp`             | MACRO          | bea → fredapi → wbgapi                                           |
| `factors`         | MACRO          | datareader → nasdaq_data_link                                    |
| `options_equity`  | EQUITY         | tradier → yfinance → polygon                                     |
| `options_crypto`  | CRYPTO         | deribit → ccxt                                                   |
| `futures_crypto`  | CRYPTO         | binance_futures → pybit → ccxt                                   |
| `liquidations`    | CRYPTO         | coinglass → binance_futures                                      |
| `news`            | EQUITY         | marketaux → finnhub → newsapi → feedparser                       |
| `news`            | CRYPTO         | cryptopanic → marketaux → feedparser                             |
| `social`          | ANY            | praw → stocktwits                                                |
| `fear_greed`      | ANY            | cnn_feargreed                                                    |
| `onchain`         | CRYPTO         | glassnode                                                        |

---

## Provider Rules

Providers are **dumb adapters** — they do exactly two things:

1. Call the external API
2. Normalize the response to the standard schema for that data type

They do **not** handle fallback logic, caching, rate limiting, or error aggregation. All of that lives in `FallbackChain`.

Every provider exposes methods matching the chain key names (`ohlcv`, `statements`, `earnings`, etc.) so `FallbackChain` can call them via `getattr(provider, method)`.

---

## Build Order

| Phase | What                          | Why                                                    |
|-------|-------------------------------|--------------------------------------------------------|
| 1     | core/ (all 8 files)           | Everything depends on this — build and test in isolation |
| 2     | technicals/ + yfinance, ccxt  | No API keys needed — validates the full engine         |
| 3     | fundamentals/ + simfin, fmp   | Core equity use case                                   |
| 4     | macro/ + fredapi, datareader  | No key for most sources                                |
| 5     | derivatives/ + deribit, ccxt  | Crypto options first (more accessible)                 |
| 6     | sentiment/ + newsapi, praw    | Last — most API-key-dependent                          |
