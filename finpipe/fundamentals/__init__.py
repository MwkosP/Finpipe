"""Fundamentals — stock categories as direct submodules (e.g. ``finpipe.fundamentals.earnings``).

Financial statement **displays**: ``finpipe.fundamentals.financials`` (income, balance, cashflow, …).

Top-level **dispatch**: ``from finpipe.fundamentals import show, showOverview`` — ``show(ticker, section=…)`` routes to
each submodule’s ``show``; ``showOverview`` lists coverage (there is no single “dump everything” yet).

Crypto-specific fundamentals can live in a separate top-level package later.
"""

from . import analyst
from . import dividends_splits
from . import earnings
from . import esg
from . import filings
from . import financial_statements
from . import financials
from . import insider
from . import institutional
from . import profile
from . import short_interest
from . import valuation_ratios
from .show import FundamentalsSection, show, showOverview

__all__ = [
    "FundamentalsSection",
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
    "show",
    "showOverview",
]
