"""Income statement — Rich display."""

from __future__ import annotations

from rich.console import Console

from .show import show as _showStatement


#other fallback call logic will be added here



def showIncome(
    ticker: str,
    *,
    console: Console | None = None,
    headlines: bool = False,
) -> None:
    """Pretty-print the consolidated income statement for ``ticker``."""
    _showStatement(ticker, "income", console=console, headlines=headlines)


def show(
    ticker: str,
    *,
    console: Console | None = None,
    headlines: bool = False,
) -> None:
    """Pretty-print the consolidated income statement for ``ticker``."""
    showIncome(ticker, console=console, headlines=headlines)
