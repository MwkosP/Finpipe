from __future__ import annotations
from typing import Any, Optional
from edgar import Company
from edgar.financials import Financials
PROVIDER_NAME = "sec_edgar"


def getCompany(ticker: str) -> Company:
    """Return an EdgarTools ``Company`` for ``ticker`` (CIK also works where supported)."""
    return Company(ticker)


def getFinancials(ticker: str) -> Optional[Financials]:
    """Latest annual financials (10-K / 20-F / 40-F), or ``None`` if unavailable."""
    return Company(ticker).get_financials()


def getQuarterlyFinancials(ticker: str) -> Optional[Financials]:
    """Latest quarterly financials (10-Q / 6-K), or ``None`` if unavailable."""
    return Company(ticker).get_quarterly_financials()


def getFilings(ticker: str, *, form: Optional[str] = None, **kwargs: Any) -> Any:
    """Company filings iterator/list from EdgarTools; pass ``form`` to filter (e.g. ``\"10-K\"``, ``\"4\"``)."""
    company = Company(ticker)
    if form is not None:
        return company.get_filings(form=form, **kwargs)
    return company.get_filings(**kwargs)


#or any other func needed for sec edgar data that will be passed to core.fallback for the FallbackChain