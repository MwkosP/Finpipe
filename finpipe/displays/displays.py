"""Shared display functions used by public domain APIs."""

from __future__ import annotations

from rich.console import Console

from finpipe.providers.sec_edgar import getFinancials

from .objects import StatementKind


def showStatement(
    ticker: str,
    kind: StatementKind,
    *,
    console: Console | None = None,
    headlines: bool = False,
) -> None:
    """Print one statement via Rich; set EdgarTools identity before use."""
    financials = getFinancials(ticker)
    if financials is None:
        raise ValueError(f"No annual financials (10-K) found for {ticker!r}")

    output = console or Console()
    match kind:
        case "income":
            output.print(financials.income_statement())
            if headlines:
                output.print()
                output.print("Headline (USD)")
                output.print("  Revenue:          ", financials.get_revenue())
                output.print("  Net income:       ", financials.get_net_income())
                output.print("  Operating income: ", financials.get_operating_income())
        case "balance":
            output.print(financials.balance_sheet())
            if headlines:
                output.print()
                output.print("Headline (USD)")
                output.print("  Total assets:        ", financials.get_total_assets())
                output.print("  Total liabilities:   ", financials.get_total_liabilities())
                output.print("  Stockholders equity: ", financials.get_stockholders_equity())
                output.print("  Current assets:      ", financials.get_current_assets())
                output.print("  Current liabilities: ", financials.get_current_liabilities())
        case "cashflow":
            output.print(financials.cash_flow_statement())
        case "equity":
            output.print(financials.statement_of_equity())
        case "comprehensive":
            output.print(financials.comprehensive_income())


__all__ = ["showStatement", "StatementKind"]
