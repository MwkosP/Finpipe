"""Cash flow statement — Rich display."""

from __future__ import annotations

from rich.console import Console

from .show import show as _showStatement


def showCashflow(
    ticker: str,
    *,
    console: Console | None = None,
) -> None:
    """Pretty-print the consolidated cash flow statement for ``ticker``."""
    _showStatement(ticker, "cashflow", console=console)


def show(
    ticker: str,
    *,
    console: Console | None = None,
) -> None:
    """Pretty-print the consolidated cash flow statement for ``ticker``."""
    showCashflow(ticker, console=console)
