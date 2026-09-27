# Technicals

## Historical OHLCV

`fetchOhlcv()` returns an `OhlcvData` object. Provider order is selected in
`finpipe.core.core`; provider functions normalize bars to `Open`, `High`, `Low`,
`Close`, and `Volume` before they reach callers.

```python
import finpipe as fp

bars = fp.technicals.fetchOhlcv("NVDA", interval="1d", period="1mo")
bars.print()                         # Rich table
frame = bars.toDataFrame()           # independent pandas DataFrame copy
print(bars.provider)                 # provider that returned the bars
print(bars.fallbackReasons)          # failures before the successful provider

# Choose one configured provider for this request:
bars = fp.technicals.fetchOhlcv("NVDA", provider="finnhub")
crypto = fp.technicals.fetchOhlcv("BTC/USDT", provider="ccxt")
```

Use `startDate` and `endDate` instead of `period` to request a date range.
Crypto symbols use Yahoo Finance notation such as `BTC-USD`. The initial
chains are configured in `finpipe/core/core.py`: equities try yfinance, Finnhub,
Alpha Vantage, then Polygon; crypto tries CCXT, then yfinance. Edit those
provider tuples to change the order. Finnhub, Alpha Vantage, and Polygon need
`FINPIPE_FINNHUB_API_KEY`, `FINPIPE_ALPHA_VANTAGE_API_KEY`, and
`FINPIPE_POLYGON_API_KEY` respectively. CCXT defaults to Binance; choose another
exchange with `providerOptions={"ccxt": {"exchangeId": "kraken"}}`.
Passing `provider=` restricts the request to that provider; omit it to use the
configured fallback order.
