"""Finnhub provider functions."""

from __future__ import annotations

import os
from urllib.parse import urlencode

import pandas as pd

from .helpers import _fetch_json, _normalize_ohlcv, _resolve_date_range

PROVIDER_NAME = "finnhub"
_RESOLUTIONS = {"1m": "1", "5m": "5", "15m": "15", "30m": "30", "60m": "60", "1h": "60", "1d": "D", "1wk": "W", "1mo": "M"}


def getOhlcv(ticker: str, *, interval: str = "1d", period: str = "1mo", start=None, end=None, autoAdjust: bool = False) -> pd.DataFrame:
    """Fetch OHLCV candles from Finnhub (requires FINPIPE_FINNHUB_API_KEY)."""
    if autoAdjust:
        raise ValueError("Finnhub candles cannot satisfy autoAdjust=True")
    api_key = os.getenv("FINPIPE_FINNHUB_API_KEY")
    if not api_key:
        raise RuntimeError("Set FINPIPE_FINNHUB_API_KEY to use Finnhub")
    resolution = _RESOLUTIONS.get(interval)
    if resolution is None:
        raise ValueError(f"Finnhub does not support interval {interval!r}")
    start_at, end_at = _resolve_date_range(start, end, period)
    params = urlencode({"symbol": ticker, "resolution": resolution, "from": int(start_at.timestamp()), "to": int(end_at.timestamp()), "token": api_key})
    payload = _fetch_json(f"https://finnhub.io/api/v1/stock/candle?{params}", PROVIDER_NAME)
    if payload.get("s") != "ok" or not payload.get("t"):
        raise ValueError(f"Finnhub returned no candles (status={payload.get('s')!r})")
    frame = pd.DataFrame({"Open": payload["o"], "High": payload["h"], "Low": payload["l"], "Close": payload["c"], "Volume": payload["v"]}, index=pd.to_datetime(payload["t"], unit="s", utc=True))
    frame = frame.loc[(frame.index >= pd.Timestamp(start_at)) & (frame.index < pd.Timestamp(end_at))]
    return _normalize_ohlcv(frame, PROVIDER_NAME)


__all__ = ["PROVIDER_NAME", "getOhlcv"]
