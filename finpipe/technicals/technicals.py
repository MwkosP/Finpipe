"""Public technicals retrieval functions."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from typing import Any

from finpipe.core import FallbackChain, getChain, runFallback
from finpipe.providers import alpha_vantage, ccxt, finnhub, polygon, yfinance

from .helpers import _validate_date_range
from .objects import OhlcvData

_PROVIDERS = {
    yfinance.PROVIDER_NAME: yfinance.getOhlcv,
    ccxt.PROVIDER_NAME: ccxt.getOhlcv,
    finnhub.PROVIDER_NAME: finnhub.getOhlcv,
    alpha_vantage.PROVIDER_NAME: alpha_vantage.getOhlcv,
    polygon.PROVIDER_NAME: polygon.getOhlcv,
}


def fetchOhlcv(
    ticker: str,
    *,
    interval: str = "1d",
    period: str = "1mo",
    startDate: date | datetime | str | None = None,
    endDate: date | datetime | str | None = None,
    autoAdjust: bool = False,
    provider: str | None = None,
    providerOptions: Mapping[str, Mapping[str, Any]] | None = None,
) -> OhlcvData:
    """Fetch historical OHLCV bars and return a Finpipe data object.

    Use ``startDate`` and ``endDate`` for an explicit range, or ``period``
    otherwise. Crypto symbols should use Yahoo Finance notation (for example
    ``BTC-USD``). Provider order comes from :mod:`finpipe.core.core`.
    """
    symbol = ticker.strip()
    if not symbol:
        raise ValueError("ticker must not be empty")
    _validate_date_range(startDate, endDate)

    chain = getChain("ohlcv", symbol)
    if provider is not None:
        if provider not in chain.providers:
            supported = ", ".join(chain.providers)
            raise ValueError(
                f"Provider {provider!r} is not configured for {chain.asset_class} OHLCV. "
                f"Configured providers: {supported}"
            )
        chain = FallbackChain(chain.key, chain.asset_class, (provider,))
    frame, selectedProvider, failures = runFallback(
        chain,
        _PROVIDERS,
        providerOptions=providerOptions,
        ticker=symbol,
        interval=interval,
        period=period,
        start=startDate,
        end=endDate,
        autoAdjust=autoAdjust,
    )
    return OhlcvData(
        data=frame,
        symbol=symbol,
        interval=interval,
        provider=selectedProvider,
        fallbackReasons=failures,
    )


def getOhlcv(ticker: str, **kwargs: Any) -> OhlcvData:
    """Alias for :func:`fetchOhlcv`."""
    return fetchOhlcv(ticker, **kwargs)


__all__ = ["fetchOhlcv", "getOhlcv"]
