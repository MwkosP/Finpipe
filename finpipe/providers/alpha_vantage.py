"""Alpha Vantage provider functions."""

from __future__ import annotations

import os
from urllib.parse import urlencode

import pandas as pd

from .helpers import _fetch_json, _normalize_ohlcv, _resolve_date_range

PROVIDER_NAME = "alpha_vantage"


def getOhlcv(ticker: str, *, interval: str = "1d", period: str = "1mo", start=None, end=None, autoAdjust: bool = False) -> pd.DataFrame:
    """Fetch daily OHLCV from Alpha Vantage (requires FINPIPE_ALPHA_VANTAGE_API_KEY)."""
    if interval != "1d":
        raise ValueError("Alpha Vantage adapter currently supports interval='1d' only")
    if autoAdjust:
        raise ValueError("Alpha Vantage raw daily data cannot satisfy autoAdjust=True")
    api_key = os.getenv("FINPIPE_ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise RuntimeError("Set FINPIPE_ALPHA_VANTAGE_API_KEY to use Alpha Vantage")
    start_at, end_at = _resolve_date_range(start, end, period)
    span_days = (end_at - start_at).days
    outputsize = "full" if span_days > 100 else "compact"
    query = urlencode({"function": "TIME_SERIES_DAILY", "symbol": ticker, "outputsize": outputsize, "apikey": api_key})
    payload = _fetch_json(f"https://www.alphavantage.co/query?{query}", PROVIDER_NAME)
    series_key = next((key for key in payload if "Time Series" in key), None)
    if series_key is None:
        reason = payload.get("Note") or payload.get("Information") or payload.get("Error Message") or "unexpected API response"
        raise ValueError(f"Alpha Vantage returned no time series: {reason}")
    frame = pd.DataFrame.from_dict(payload[series_key], orient="index")
    frame = frame.rename(columns={"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume": "Volume"})
    frame.index = pd.to_datetime(frame.index, utc=True)
    frame = frame.apply(pd.to_numeric).sort_index()
    frame = frame.loc[(frame.index >= start_at) & (frame.index < end_at)]
    if not frame.empty and frame.index.min() > pd.Timestamp(start_at) + pd.Timedelta(days=3):
        raise ValueError("Alpha Vantage response does not cover the requested start date")
    return _normalize_ohlcv(frame, PROVIDER_NAME)


__all__ = ["PROVIDER_NAME", "getOhlcv"]
