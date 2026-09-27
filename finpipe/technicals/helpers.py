"""Internal validation and transformation helpers for technicals APIs."""

from __future__ import annotations

from datetime import date, datetime

import pandas as pd


def _validate_date_range(start_date: date | datetime | str | None, end_date: date | datetime | str | None) -> None:
    """Reject an inverted explicit date range before provider calls."""
    if start_date is not None and end_date is not None:
        if pd.Timestamp(start_date) >= pd.Timestamp(end_date):
            raise ValueError("startDate must be earlier than endDate")
