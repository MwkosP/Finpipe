"""Financial statements — yfinance, alpha_vantage, fmpsdk, simfinapi."""

from __future__ import annotations

from rich.console import Console

from finpipe.fundamentals._show_util import _show_placeholder


def show(ticker: str, *, console: Console | None = None) -> None:
    """Pretty-print normalized statement data for ``ticker`` (when implemented).

    For consolidated SEC/XBRL Rich tables today, use ``fundamentals.show(..., section='financials', kind=…)``.
    """
    _show_placeholder(
        "financial_statements",
        ticker,
        hint="For consolidated statement tables, use fundamentals.show(..., section='financials', kind='income').",
        console=console,
    )
