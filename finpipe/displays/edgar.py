"""Pretty-print EdgarTools financial statements (Rich panels, SEC viewer style)."""

from __future__ import annotations
from typing import Literal
from edgar import Company
from rich.console import Console

StatementKind = Literal["income", "balance", "cashflow", "equity", "comprehensive"]


def show_statement(
    ticker: str,
    kind: StatementKind,
    *,
    console: Console | None = None,
    headlines: bool = False,
) -> None:
    """Print one statement via Rich for ``ticker``. Call ``set_identity`` before this (or set ``EDGAR_IDENTITY``).

    ``headlines`` only applies to income and balance.
    """
    financials = Company(ticker).get_financials()
    if financials is None:
        raise ValueError(f"No annual financials (10-K) found for {ticker!r}")

    c = console or Console()
    match kind:
        case "income":
            c.print(financials.income_statement())
            if headlines:
                print()
                print("Headline (USD)")
                print("  Revenue:          ", financials.get_revenue())
                print("  Net income:       ", financials.get_net_income())
                print("  Operating income: ", financials.get_operating_income())
        case "balance":
            c.print(financials.balance_sheet())
            if headlines:
                print()
                print("Headline (USD)")
                print("  Total assets:        ", financials.get_total_assets())
                print("  Total liabilities:   ", financials.get_total_liabilities())
                print("  Stockholders equity: ", financials.get_stockholders_equity())
                print("  Current assets:      ", financials.get_current_assets())
                print("  Current liabilities: ", financials.get_current_liabilities())
        case "cashflow":
            c.print(financials.cashflow_statement())
        case "equity":
            c.print(financials.statement_of_equity())
        case "comprehensive":
            c.print(financials.comprehensive_income())
