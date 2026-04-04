"""Dividends and splits — yfinance, finnhub, fmpsdk, pandas-datareader."""

from __future__ import annotations

from rich.console import Console

from finpipe.fundamentals._show_util import _show_placeholder


def show(ticker: str, *, console: Console | None = None) -> None:
    """Pretty-print dividends and splits for ``ticker`` (when implemented)."""
    _show_placeholder("dividends_splits", ticker, console=console)
