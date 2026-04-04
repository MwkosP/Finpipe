"""Statement of changes in equity — Rich display."""

from __future__ import annotations

from rich.console import Console

from .show import show as _showStatement


def showEquity(
    ticker: str,
    *,
    console: Console | None = None,
) -> None:
    """Pretty-print the statement of changes in equity for ``ticker``."""
    _showStatement(ticker, "equity", console=console)


def show(
    ticker: str,
    *,
    console: Console | None = None,
) -> None:
    """Pretty-print the statement of changes in equity for ``ticker``."""
    showEquity(ticker, console=console)
