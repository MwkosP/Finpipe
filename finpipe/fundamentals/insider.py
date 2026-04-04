"""Insider transactions — yfinance, finnhub, fmpsdk, sec-edgar-downloader."""

from __future__ import annotations

from rich.console import Console

from finpipe.fundamentals._show_util import _show_placeholder


def show(ticker: str, *, console: Console | None = None) -> None:
    """Pretty-print insider activity for ``ticker`` (when implemented)."""
    _show_placeholder("insider", ticker, console=console)
