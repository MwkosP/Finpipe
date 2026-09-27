"""Internal normalization helpers shared by provider adapters."""

from __future__ import annotations

import pandas as pd
from datetime import datetime, timedelta, timezone
import json
import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def _normalize_ohlcv(frame: pd.DataFrame, provider_name: str) -> pd.DataFrame:
    """Normalize a provider frame to Finpipe's canonical OHLCV columns."""
    if frame is None or frame.empty:
        raise ValueError(f"{provider_name} returned no OHLCV data")
    if isinstance(frame.columns, pd.MultiIndex):
        frame = frame.copy()
        frame.columns = frame.columns.get_level_values(0)
    by_lower = {str(column).lower(): column for column in frame.columns}
    required = ("open", "high", "low", "close", "volume")
    missing = [column for column in required if column not in by_lower]
    if missing:
        raise ValueError(f"{provider_name} response is missing OHLCV columns: {missing}")
    normalized = frame.loc[:, [by_lower[column] for column in required]].copy()
    normalized.columns = ["Open", "High", "Low", "Close", "Volume"]
    normalized.index.name = normalized.index.name or "Datetime"
    return normalized


def _resolve_date_range(start, end, period: str) -> tuple[datetime, datetime]:
    """Resolve an explicit or relative range to UTC datetimes."""
    end_at = pd.Timestamp(end).to_pydatetime() if end is not None else datetime.now(timezone.utc)
    if end_at.tzinfo is None:
        end_at = end_at.replace(tzinfo=timezone.utc)
    if start is not None:
        start_at = pd.Timestamp(start).to_pydatetime()
        if start_at.tzinfo is None:
            start_at = start_at.replace(tzinfo=timezone.utc)
        return start_at, end_at

    match = re.fullmatch(r"(\d+)(d|wk|mo|y)", period.lower())
    if match:
        count = int(match.group(1))
        unit = match.group(2)
        days = count * {"d": 1, "wk": 7, "mo": 30, "y": 365}[unit]
    elif period.lower() == "ytd":
        return datetime(end_at.year, 1, 1, tzinfo=timezone.utc), end_at
    elif period.lower() == "max":
        days = 365 * 20
    else:
        raise ValueError(f"Unsupported period: {period!r}")
    return end_at - timedelta(days=days), end_at


def _fetch_json(url: str, provider_name: str) -> dict:
    """Fetch a JSON API response without leaking query-string credentials."""
    try:
        with urlopen(url, timeout=20) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"{provider_name} request failed with HTTP {exc.code}") from None
    except URLError as exc:
        raise RuntimeError(f"{provider_name} request failed: {exc.reason}") from None
