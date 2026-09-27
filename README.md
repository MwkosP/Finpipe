# Finpipe

![Finpipe wordmark](assets/finpipe.svg)

A unified Python API that pipes financial data from many providers into one place.

---

## Overview

Finpipe is built to cover nearly every financial-data need through a single interface: technicals, fundamentals, macroeconomic data, derivatives, sentiment, news, prediction markets, and provider integrations. Each domain can use a shared fallback system, so applications ask Finpipe for data instead of managing provider-specific APIs themselves.

## Quick Start

```bash
git clone https://github.com/MwkosP/Finpipe.git
cd Finpipe
uv sync
```

```python
import finpipe as fp

bars = fp.technicals.fetchOhlcv("NVDA", interval="1d", period="1mo")
bars.print()

print(bars.provider)
print(bars.toDataFrame().tail())
```

Crypto pairs use exchange notation:

```python
btc = fp.technicals.fetchOhlcv("BTC/USDT", interval="1d", period="1mo")
```

## Coverage

- **Technicals** — OHLCV, market data, order books, trades, volume, and streaming
- **Fundamentals** — financial statements, filings, ratios, earnings, company data, and ownership data
- **Macro** — economic indicators and market context
- **Derivatives** — options and futures data
- **Sentiment** — social data and market sentiment
- **News** — financial headlines, feeds, and event data
- **Prediction Markets** — market probabilities and event contracts
- **Providers** — one provider module per data source, with shared fallback chains

The current API includes normalized OHLCV retrieval with automatic fallback and SEC financial-statement displays. The remaining domains are being built under the same unified interface.

This library uses the [uv](https://docs.astral.sh/uv/) package manager.

## License

MIT License.
