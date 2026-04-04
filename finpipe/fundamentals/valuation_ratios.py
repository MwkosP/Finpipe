"""Valuation ratios and key metrics — yfinance, finnhub, fmpsdk, simfinapi."""

from __future__ import annotations

from rich.console import Console

from finpipe.fundamentals._show_util import _show_placeholder


def show(ticker: str, *, console: Console | None = None) -> None:
    """Pretty-print valuation ratios for ``ticker`` (when implemented)."""
    _show_placeholder("valuation_ratios", ticker, console=console)
