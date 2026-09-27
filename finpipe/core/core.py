"""Shared provider chain registry and fallback engine."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from .objects import AssetClass, FallbackChain, FallbackError, ProviderError

_CHAINS: dict[tuple[str, AssetClass], FallbackChain] = {
    # Edit these tuples to reorder or add providers.
    ("ohlcv", "EQUITY"): FallbackChain(
        "ohlcv", "EQUITY", ("yfinance", "finnhub", "alpha_vantage", "polygon")
    ),
    ("ohlcv", "CRYPTO"): FallbackChain("ohlcv", "CRYPTO", ("ccxt", "yfinance")),
}


def detectAssetClass(ticker: str) -> AssetClass:
    """Classify common crypto symbols; treat all other symbols as equities."""
    symbol = ticker.strip().upper()
    if "/" in symbol or symbol.endswith(("-PERP", "-USDT", "-USDC", "-USD")):
        return "CRYPTO"
    return "EQUITY"


def getChain(chainKey: str, ticker: str, *, assetClass: AssetClass | None = None) -> FallbackChain:
    """Return the configured provider chain for a request."""
    asset_class = assetClass or detectAssetClass(ticker)
    try:
        return _CHAINS[(chainKey, asset_class)]
    except KeyError as exc:
        raise ValueError(f"No fallback chain configured for {chainKey!r} / {asset_class!r}") from exc


def runFallback(
    chain: FallbackChain,
    providers: Mapping[str, Callable[..., Any]],
    *,
    providerOptions: Mapping[str, Mapping[str, Any]] | None = None,
    **kwargs: Any,
) -> tuple[Any, str, tuple[ProviderError, ...]]:
    """Call providers in order, returning data, selected provider, and earlier failures."""
    failures: list[ProviderError] = []
    for provider_name in chain.providers:
        provider = providers.get(provider_name)
        if provider is None:
            failures.append(ProviderError(provider_name, "adapter is not registered"))
            continue
        try:
            options = (providerOptions or {}).get(provider_name, {})
            result = provider(**kwargs, **options)
            if result is None or (hasattr(result, "empty") and result.empty):
                raise ValueError("provider returned no data")
            return result, provider_name, tuple(failures)
        except Exception as exc:
            failures.append(ProviderError(provider_name, str(exc) or type(exc).__name__))
    raise FallbackError(chain.key, failures)


__all__ = ["detectAssetClass", "getChain", "runFallback"]
