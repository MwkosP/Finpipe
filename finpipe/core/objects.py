"""Core data classes and exceptions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AssetClass = Literal["EQUITY", "CRYPTO", "ANY"]


@dataclass(frozen=True)
class FallbackChain:
    key: str
    asset_class: AssetClass
    providers: tuple[str, ...]


class FinpipeError(Exception):
    """Base class for public Finpipe errors."""


class ProviderError(FinpipeError):
    """A provider could not return usable data."""

    def __init__(self, provider: str, message: str) -> None:
        self.provider = provider
        super().__init__(f"{provider}: {message}")


class FallbackError(FinpipeError):
    """Every provider in a fallback chain failed."""

    def __init__(self, chain_key: str, failures: list[ProviderError]) -> None:
        self.chain_key = chain_key
        self.failures = failures
        details = "; ".join(str(error) for error in failures)
        super().__init__(f"All providers failed for {chain_key!r}: {details}")
