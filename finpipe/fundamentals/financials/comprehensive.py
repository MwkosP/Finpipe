"""Statement of comprehensive income — Rich display."""

from __future__ import annotations

from rich.console import Console

from .show import show as _showStatement


def showComprehensive(
    ticker: str,
    *,
    console: Console | None = None,
) -> None:
    """Pretty-print the statement of comprehensive income for ``ticker``."""
    _showStatement(ticker, "comprehensive", console=console)


def show(
    ticker: str,
    *,
    console: Console | None = None,
) -> None:
    """Pretty-print the statement of comprehensive income for ``ticker``."""
    showComprehensive(ticker, console=console)
