"""SEC filings — sec-edgar-downloader, finnhub (links), fmpsdk, SEC EDGAR API."""

from __future__ import annotations

from rich.console import Console

from finpipe.fundamentals._show_util import _show_placeholder


def show(ticker: str, *, console: Console | None = None) -> None:
    """Pretty-print filing index / links for ``ticker`` (when implemented)."""
    _show_placeholder("filings", ticker, console=console)
