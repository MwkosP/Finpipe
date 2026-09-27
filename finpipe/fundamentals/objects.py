"""Shared public type aliases for fundamentals APIs."""

from typing import Literal

from finpipe.displays.objects import StatementKind

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
