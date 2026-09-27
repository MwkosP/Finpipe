"""Polygon provider functions."""

from __future__ import annotations

import os
from urllib.parse import quote, urlencode

import pandas as pd

from .helpers import _fetch_json, _normalize_ohlcv, _resolve_date_range

PROVIDER_NAME = "polygon"
_INTERVALS = {"1m": (1, "minute"), "5m": (5, "minute"), "15m": (15, "minute"), "30m": (30, "minute"), "1h": (1, "hour"), "1d": (1, "day"), "1wk": (1, "week"), "1mo": (1, "month")}


def getOhlcv(ticker: str, *, interval: str = "1d", period: str = "1mo", start=None, end=None, autoAdjust: bool = False) -> pd.DataFrame:
    """Fetch stock aggregates from Polygon (requires FINPIPE_POLYGON_API_KEY)."""
    api_key = os.getenv("FINPIPE_POLYGON_API_KEY")
    if not api_key:
        raise RuntimeError("Set FINPIPE_POLYGON_API_KEY to use Polygon")
    multiplier, timespan = _INTERVALS.get(interval, (None, None))
    if multiplier is None:
        raise ValueError(f"Polygon does not support interval {interval!r}")
    start_at, end_at = _resolve_date_range(start, end, period)
    path = f"/v2/aggs/ticker/{quote(ticker, safe='')}/range/{multiplier}/{timespan}/{start_at.date()}/{end_at.date()}"
    query = urlencode({"adjusted": str(autoAdjust).lower(), "sort": "asc", "limit": 50000, "apiKey": api_key})
    payload = _fetch_json(f"https://api.polygon.io{path}?{query}", PROVIDER_NAME)
    rows = payload.get("results") or []
    if not rows:
        raise ValueError(f"Polygon returned no aggregates: {payload.get('status', 'empty response')}")
    frame = pd.DataFrame(rows).rename(columns={"o": "Open", "h": "High", "l": "Low", "c": "Close", "v": "Volume", "t": "timestamp"})
    frame.index = pd.to_datetime(frame.pop("timestamp"), unit="ms", utc=True)
    frame = frame.loc[(frame.index >= pd.Timestamp(start_at)) & (frame.index < pd.Timestamp(end_at))]
    return _normalize_ohlcv(frame, PROVIDER_NAME)


__all__ = ["PROVIDER_NAME", "getOhlcv"]
