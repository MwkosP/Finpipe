# Providers

## All providers (reference)

- alpha_vantage
- ccxt
- ccxt_pro
- coingecko
- finnhub
- fmpsdk
- ib_insync
- pandas-datareader
- polygon
- SEC EDGAR API (direct)
- sec-edgar-downloader
- simfinapi
- tardis-python
- yfinance


---

## Technicals

- OHLCV Historical (yfinance, finnhub, alpha_vantage, polygon, ccxt, tardis-python)
- Orderbook L1 / L2 depth — crypto: ccxt, tardis-python | stocks/futures: polygon
- Tick / trade data — crypto: ccxt, tardis-python | stocks: polygon, ib_insync
- Volume — crypto: per exchange ccxt | aggregated + market dominance: coingecko | tick-level: tardis-python | stocks: yfinance, polygon, finnhub, ib_insync
- Real-time streaming / WebSockets (finnhub, ccxt_pro, ib_insync)

---

## Fundamentals (Stocks)


- Financial Statements (yfinance, alpha_vantage, fmpsdk, simfinapi)
- Valuation Ratios & Key Metrics (yfinance, finnhub, fmpsdk, simfinapi)
- Earnings — EPS, Surprises, Calendar, Estimates (yfinance, finnhub, fmpsdk, alpha_vantage)
- Analyst Recommendations & Price Targets (yfinance, finnhub, fmpsdk)
- Insider Transactions (yfinance, finnhub, fmpsdk, sec-edgar-downloader)
- Institutional Holdings (yfinance, finnhub, fmpsdk)
- SEC Filings (sec-edgar-downloader, finnhub links only, fmpsdk, SEC EDGAR API direct)
- Dividends & Splits (yfinance, finnhub, fmpsdk, pandas-datareader)
- Short Interest (yfinance, finnhub, fmpsdk)
- ESG (yfinance, finnhub)
- Company Profile / Sector / Industry (yfinance, finnhub, fmpsdk)

---

# ---------------------
Technicals(OHLCV, order books, trades, streaming):
ccxt/ccxt
bmoscon/cryptofeed
ranaroussi/yfinance


Fundamentals:
dgunning/edgartools
JerBouma/FinanceToolkit
ranaroussi/yfinance
lit26/finvizfinance

News:
alex9smith/gdelt-doc-api
lit26/finvizfinance
ranaroussi/yfinance
kurtmckee/feedparser
kurtmckee/feedparser


Macro: 
mortada/fredapi
pydata/pandas-datareader
OpenBB-finance/OpenBB


PMs:



onchain:
mempool.space API
Blockchain.com Charts API
Coin Metrics Community API
DefiLlama API
DexScreener API
GeckoTerminal API
Etherscan API V2
Public RPC endpoints via web3.py
Dune API



Derivatives:
ccxt/ccxt
ranaroussi/yfinance
vollib/py_vollib
OpenBB-finance/OpenBB


Sentiment:
praw-dev/praw
cjhutto/vaderSentiment
santiment/sanpy
GeneralMills/pytrends
The alternative.me Fear & Greed API is a single free endpoint, so no repo is needed








# ---------------
Yes, and it's worth doing, because free APIs break constantly. The standard setup is two separate pipelines in GitHub Actions.

1. On every push/PR: fast tests that never hit real APIs
Record real API responses once and replay them in tests, using pytest-recording (vcrpy). This tests your parsing and normalization without depending on the internet, so PRs don't fail because Yahoo had a bad minute.

2. On a schedule (e.g. nightly): live provider health checks
This is the "is any API broken?" check. The key design rule: test each provider individually with fallback turned off. Otherwise your fallback system silently hides the broken provider, and the test passes while one of your sources is dead.

A live test, parametrized per provider:

python
@pytest.mark.live
@pytest.mark.parametrize("provider", ["yfinance", "binance", "kraken"])
def test_ohlcv(provider):
    bars = fp.technicals.fetchOhlcv("BTC/USDT", interval="1d", period="5d",
                                    provider=provider, fallback=False)
    df = bars.toDataFrame()
    assert len(df) > 0
    assert {"open", "high", "low", "close", "volume"} <= set(df.columns)

Assert the shape of the data (non-empty, expected columns, sane types, recent timestamps), never exact values, since those change every day.

The workflow file (.github/workflows/provider-health.yml):

yaml
on:
  schedule: [{cron: "0 6 * * *"}]
  workflow_dispatch:
jobs:
  live:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv sync
      - run: uv run pytest -m live -v
        env:
          FRED_API_KEY: ${{ secrets.FRED_API_KEY }}

API keys go in repo Settings → Secrets, never in code. workflow_dispatch lets you trigger the run manually.

Useful extras:

Auto-open an issue on failure: add a step with if: failure() that runs gh issue create, so you get notified with the failing provider names.
Run your examples too: a test that loops over examples/*.py and runs each with subprocess, failing if any exits with an error. This keeps the README examples honest.
Health dashboard: write the results per provider (ok / failing / latency) to a JSON file and publish it with GitHub Pages or a README badge. Users love seeing which providers are currently up, and it looks professional.

Gotchas specific to your providers:

GitHub runners are in the US. Binance.com blocks US IPs (HTTP 451), so Binance tests will fail on GitHub even when the API is fine. Test Binance through binance.us, mark it as an expected skip on CI, or use a self-hosted runner (e.g. your own machine in Greece).
Yahoo and some other free sources rate-limit or block datacenter IPs. Add one retry with backoff before calling a provider broken, and keep the number of live calls small.
Scheduled workflows get disabled automatically in public repos after 60 days without repository activity. A commit or manual run re-enables them.
Flaky vs broken: treat a single failure as a warning and 2–3 consecutive failures as "broken." Otherwise you'll get noise from temporary outages.