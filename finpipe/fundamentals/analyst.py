"""Analyst recommendations and price targets — yfinance, finnhub, fmpsdk."""

from __future__ import annotations

from rich.console import Console

from finpipe.fundamentals._show_util import _show_placeholder


def show(ticker: str, *, console: Console | None = None) -> None:
    """Pretty-print analyst coverage for ``ticker`` (when implemented)."""
    _show_placeholder("analyst", ticker, console=console)
