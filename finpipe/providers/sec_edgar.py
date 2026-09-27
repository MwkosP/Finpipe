"""SEC EDGAR provider functions backed by EdgarTools."""

from __future__ import annotations

from typing import Any, Optional

from edgar import Company
from edgar.financials import Financials

PROVIDER_NAME = "sec_edgar"


def getCompany(ticker: str) -> Company:
    """Return an EdgarTools Company for a ticker or supported CIK."""
    return Company(ticker)


def getFinancials(ticker: str) -> Optional[Financials]:
    """Return latest annual financials, or None if unavailable."""
    return Company(ticker).get_financials()


def getQuarterlyFinancials(ticker: str) -> Optional[Financials]:
    """Return latest quarterly financials, or None if unavailable."""
    return Company(ticker).get_quarterly_financials()


def getFilings(ticker: str, *, form: Optional[str] = None, **kwargs: Any) -> Any:
    """Return company filings, optionally filtered by SEC form type."""
    company = Company(ticker)
    if form is not None:
        return company.get_filings(form=form, **kwargs)
    return company.get_filings(**kwargs)


__all__ = ["PROVIDER_NAME", "getCompany", "getFinancials", "getQuarterlyFinancials", "getFilings"]
