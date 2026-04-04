"""Balance sheet — Rich display."""

from __future__ import annotations

from rich.console import Console

from .show import show as _showStatement


def showBalance(
    ticker: str,
    *,
    console: Console | None = None,
    headlines: bool = False,
) -> None:
    """Pretty-print the consolidated balance sheet for ``ticker``."""
    _showStatement(ticker, "balance", console=console, headlines=headlines)


def show(
    ticker: str,
    *,
    console: Console | None = None,
    headlines: bool = False,
) -> None:
    """Pretty-print the consolidated balance sheet for ``ticker``."""
    showBalance(ticker, console=console, headlines=headlines)
