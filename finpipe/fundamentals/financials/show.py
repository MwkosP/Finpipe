"""Unified ``show(ticker, kind)`` for financial statements (Rich)."""

from __future__ import annotations
from rich.console import Console
from finpipe.displays.edgar import StatementKind, show_statement

__all__ = ["StatementKind", "show"]


def show(
    ticker: str,
    kind: StatementKind,
    *,
    console: Console | None = None,
    headlines: bool = False,
) -> None:
    """Pretty-print one statement. ``kind``: ``income`` | ``balance`` | ``cashflow`` | ``equity`` | ``comprehensive``.

    ``headlines`` only applies to ``income`` and ``balance``. Call ``set_identity`` / ``EDGAR_IDENTITY`` before use (current implementation uses EdgarTools).
    """
    show_statement(ticker, kind, console=console, headlines=headlines)
