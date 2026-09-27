"""CCXT exchange provider functions."""

from __future__ import annotations

import pandas as pd

from .helpers import _normalize_ohlcv, _resolve_date_range

PROVIDER_NAME = "ccxt"


def getOhlcv(
    ticker: str,
    *,
    interval: str = "1d",
    period: str = "1mo",
    start=None,
    end=None,
    autoAdjust: bool = False,
    exchangeId: str = "binance",
) -> pd.DataFrame:
    """Fetch OHLCV from a public CCXT exchange endpoint."""
    if autoAdjust:
        raise ValueError("CCXT candles cannot satisfy autoAdjust=True")
    try:
        import ccxt
    except ImportError as exc:
        raise RuntimeError("CCXT is required; install it with `uv add ccxt`") from exc
    exchange_type = getattr(ccxt, exchangeId, None)
    if exchange_type is None or exchangeId not in ccxt.exchanges:
        raise ValueError(f"Unknown CCXT exchange: {exchangeId!r}")
    exchange = exchange_type({"enableRateLimit": True})
    try:
        if not exchange.has.get("fetchOHLCV"):
            raise ValueError(f"{exchangeId} does not support OHLCV")
        start_at, end_at = _resolve_date_range(start, end, period)
        timeframe = {"1wk": "1w", "1mo": "1M"}.get(interval, interval)
        candles = exchange.fetch_ohlcv(
            ticker,
            timeframe=timeframe,
            since=int(start_at.timestamp() * 1000),
            limit=1000,
        )
        if not candles:
            raise ValueError(f"No OHLCV data returned for {ticker!r}")
        frame = pd.DataFrame(candles, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"])
        frame.index = pd.to_datetime(frame.pop("timestamp"), unit="ms", utc=True)
        frame = frame.loc[(frame.index >= pd.Timestamp(start_at)) & (frame.index < pd.Timestamp(end_at))]
        return _normalize_ohlcv(frame, PROVIDER_NAME)
    finally:
        exchange.close()


__all__ = ["PROVIDER_NAME", "getOhlcv"]
