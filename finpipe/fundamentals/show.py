"""Top-level ``show`` for ``fundamentals`` — dispatch by section + ``showOverview``."""

from __future__ import annotations

import importlib
from typing import Literal

from rich.console import Console
from rich.table import Table

from finpipe.fundamentals.financials.show import StatementKind, show as showFinancials

FundamentalsSection = Literal[
    "analyst",
    "dividends_splits",
    "earnings",
    "esg",
    "filings",
    "financial_statements",
    "financials",
    "insider",
    "institutional",
    "profile",
    "short_interest",
    "valuation_ratios",
]

_SECTIONS: frozenset[str] = frozenset(
    (
        "analyst",
        "dividends_splits",
        "earnings",
        "esg",
        "filings",
        "financial_statements",
        "financials",
        "insider",
        "institutional",
        "profile",
        "short_interest",
        "valuation_ratios",
    )
)

__all__ = ["FundamentalsSection", "show", "showOverview"]


def show(
    ticker: str,
    section: FundamentalsSection,
    *,
    kind: StatementKind | None = None,
    headlines: bool = False,
    console: Console | None = None,
) -> None:
    """Pretty-print one fundamentals area. ``section`` names the submodule (e.g. ``financials``, ``earnings``).

    For ``section='financials'``, pass ``kind`` (``income`` | ``balance`` | ...). Other sections use their submodule
    ``show`` (placeholders until wired to data + Rich).
    """
    if section not in _SECTIONS:
        raise ValueError(f"Unknown fundamentals section: {section!r}. Expected one of {sorted(_SECTIONS)}.")

    if section == "financials":
        if kind is None:
            raise TypeError(
                "fundamentals.show(..., section='financials') requires kind= "
                "(e.g. 'income', 'balance', 'cashflow', 'equity', 'comprehensive')."
            )
        showFinancials(ticker, kind, console=console, headlines=headlines)
        return

    mod = importlib.import_module(f"finpipe.fundamentals.{section}")
    show_fn = getattr(mod, "show", None)
    if show_fn is None:
        raise RuntimeError(f"finpipe.fundamentals.{section} has no show()")
    show_fn(ticker, console=console)


def showOverview(ticker: str, *, console: Console | None = None) -> None:
    """Print what each fundamentals area covers and how to call ``show`` (cannot load all datasets in one go yet)."""
    c = console or Console()
    table = Table(title=f"Fundamentals - {ticker}", show_header=True, header_style="bold")
    table.add_column("Section", style="cyan", no_wrap=True)
    table.add_column("Status")
    table.add_column("Example")

    rows: list[tuple[str, str, str]] = [
        ("financials", "implemented (SEC XBRL via EdgarTools)", "show(t, 'financials', kind='income')"),
        ("analyst", "placeholder", "show(t, 'analyst')"),
        ("dividends_splits", "placeholder", "show(t, 'dividends_splits')"),
        ("earnings", "placeholder", "show(t, 'earnings')"),
        ("esg", "placeholder", "show(t, 'esg')"),
        ("filings", "placeholder", "show(t, 'filings')"),
        ("financial_statements", "placeholder (see financials for tables)", "show(t, 'financial_statements')"),
        ("insider", "placeholder", "show(t, 'insider')"),
        ("institutional", "placeholder", "show(t, 'institutional')"),
        ("profile", "placeholder", "show(t, 'profile')"),
        ("short_interest", "placeholder", "show(t, 'short_interest')"),
        ("valuation_ratios", "placeholder", "show(t, 'valuation_ratios')"),
    ]
    for section, status, example in rows:
        table.add_row(section, status, example)

    c.print(table)
    c.print(
        "[dim]There is no single 'show everything' dump yet: fundamentals differ by source and size. "
        "Use show(ticker, section=...) per area, or import finpipe.fundamentals.<module> and call show.[/dim]"
    )
