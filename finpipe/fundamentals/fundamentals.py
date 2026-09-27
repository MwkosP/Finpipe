"""Public fundamentals functions."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from finpipe.displays import showStatement

from .helpers import _show_placeholder
from .objects import FundamentalsSection, StatementKind

__all__ = [
    "FundamentalsSection",
    "StatementKind",
    "show",
    "showOverview",
    "showFinancials",
    "showIncome",
    "showBalance",
    "showCashflow",
    "showEquity",
    "showComprehensive",
]


def showFinancials(
    ticker: str,
    kind: StatementKind,
    *,
    console: Console | None = None,
    headlines: bool = False,
) -> None:
    """Print an SEC financial statement using EdgarTools."""
    showStatement(ticker, kind, console=console, headlines=headlines)


def showIncome(ticker: str, *, console: Console | None = None, headlines: bool = False) -> None:
    """Print the income statement."""
    showFinancials(ticker, "income", console=console, headlines=headlines)


def showBalance(ticker: str, *, console: Console | None = None, headlines: bool = False) -> None:
    """Print the balance sheet."""
    showFinancials(ticker, "balance", console=console, headlines=headlines)


def showCashflow(ticker: str, *, console: Console | None = None) -> None:
    """Print the cash flow statement."""
    showFinancials(ticker, "cashflow", console=console)


def showEquity(ticker: str, *, console: Console | None = None) -> None:
    """Print the statement of changes in equity."""
    showFinancials(ticker, "equity", console=console)


def showComprehensive(ticker: str, *, console: Console | None = None) -> None:
    """Print the statement of comprehensive income."""
    showFinancials(ticker, "comprehensive", console=console)


def show(
    ticker: str,
    section: FundamentalsSection,
    *,
    kind: StatementKind | None = None,
    headlines: bool = False,
    console: Console | None = None,
) -> None:
    """Print one fundamentals area by section name."""
    if section == "financials":
        if kind is None:
            raise TypeError("section='financials' requires kind= (for example, kind='income')")
        showFinancials(ticker, kind, console=console, headlines=headlines)
        return
    if section not in FundamentalsSection.__args__:
        raise ValueError(f"Unknown fundamentals section: {section!r}")
    if section == "financial_statements":
        _show_placeholder(
            section,
            ticker,
            hint="Use showFinancials(ticker, kind) for SEC statement tables.",
            console=console,
        )
        return
    _show_placeholder(section, ticker, console=console)


def showOverview(ticker: str, *, console: Console | None = None) -> None:
    """Print current fundamentals coverage and example calls."""
    output = console or Console()
    table = Table(title=f"Fundamentals - {ticker}", show_header=True, header_style="bold")
    table.add_column("Section", style="cyan", no_wrap=True)
    table.add_column("Status")
    table.add_column("Example")
    rows = [
        ("financials", "implemented (SEC XBRL via EdgarTools)", "showFinancials(t, 'income')"),
        ("analyst", "placeholder", "show(t, 'analyst')"),
        ("dividends_splits", "placeholder", "show(t, 'dividends_splits')"),
        ("earnings", "placeholder", "show(t, 'earnings')"),
        ("esg", "placeholder", "show(t, 'esg')"),
        ("filings", "placeholder", "show(t, 'filings')"),
        ("financial_statements", "placeholder", "show(t, 'financial_statements')"),
        ("insider", "placeholder", "show(t, 'insider')"),
        ("institutional", "placeholder", "show(t, 'institutional')"),
        ("profile", "placeholder", "show(t, 'profile')"),
        ("short_interest", "placeholder", "show(t, 'short_interest')"),
        ("valuation_ratios", "placeholder", "show(t, 'valuation_ratios')"),
    ]
    for row in rows:
        table.add_row(*row)
    output.print(table)
