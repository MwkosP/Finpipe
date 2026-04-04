"""Earnings (EPS, surprises, calendar, estimates) — yfinance, finnhub, fmpsdk, alpha_vantage."""

from __future__ import annotations

from rich.console import Console

from finpipe.fundamentals._show_util import _show_placeholder


def show(ticker: str, *, console: Console | None = None) -> None:
    """Pretty-print earnings-related data for ``ticker`` (when implemented)."""
    _show_placeholder("earnings", ticker, console=console)
