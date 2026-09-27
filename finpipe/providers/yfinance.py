"""Yahoo Finance provider functions."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .helpers import _normalize_ohlcv

PROVIDER_NAME = "yfinance"


def getOhlcv(
    ticker: str,
    *,
    interval: str = "1d",
    period: str = "1mo",
    start: Any = None,
    end: Any = None,
    autoAdjust: bool = False,
) -> pd.DataFrame:
    """Fetch and normalize historical OHLCV bars from yfinance."""
    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError("yfinance is required; install it with `uv add yfinance`") from exc

    options: dict[str, Any] = {"interval": interval, "auto_adjust": autoAdjust}
    if start is not None:
        options["start"] = start
    if end is not None:
        options["end"] = end
    if start is None and end is None:
        options["period"] = period
    return _normalize_ohlcv(yf.Ticker(ticker).history(**options), PROVIDER_NAME)


__all__ = ["PROVIDER_NAME", "getOhlcv"]
