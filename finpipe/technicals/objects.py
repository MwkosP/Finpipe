"""Data classes returned by technicals APIs."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd
from rich.console import Console
from rich.table import Table

from finpipe.core.objects import ProviderError

OHLCV_COLUMNS = ("Open", "High", "Low", "Close", "Volume")


@dataclass
class OhlcvData:
    """Normalized OHLCV bars with provider provenance and display helpers."""

    data: pd.DataFrame
    symbol: str
    interval: str
    provider: str
    fallbackReasons: tuple[ProviderError, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        missing = set(OHLCV_COLUMNS).difference(self.data.columns)
        if missing:
            raise ValueError(f"OHLCV data is missing required columns: {sorted(missing)}")
        self.data = self.data.loc[:, list(OHLCV_COLUMNS)].copy()
        self.data.index.name = self.data.index.name or "Datetime"

    def toDataFrame(self) -> pd.DataFrame:
        """Return a copy of the normalized bars as a pandas DataFrame."""
        return self.data.copy()

    def print(self, *, console: Console | None = None, maxRows: int = 20) -> None:
        """Render the bars as a Rich table."""
        if maxRows < 1:
            raise ValueError("maxRows must be at least 1")
        output = console or Console()
        table = Table(title=f"{self.symbol} OHLCV · {self.interval} · {self.provider}")
        table.add_column("Datetime", style="cyan", no_wrap=True)
        for column in OHLCV_COLUMNS:
            table.add_column(column, justify="right")
        shown = self.data.tail(maxRows)
        for timestamp, row in shown.iterrows():
            values = [str(timestamp)]
            values.extend("" if pd.isna(row[name]) else f"{row[name]:,.6g}" for name in OHLCV_COLUMNS)
            table.add_row(*values)
        output.print(table)
        if len(self.data) > len(shown):
            output.print(f"[dim]Showing latest {len(shown)} of {len(self.data)} bars.[/dim]")

    def __len__(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        return (
            f"OhlcvData(symbol={self.symbol!r}, interval={self.interval!r}, "
            f"provider={self.provider!r}, bars={len(self.data)})"
        )
