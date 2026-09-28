"""Data objects emitted by technicals streaming APIs."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from rich.console import Console
from rich.table import Table


@dataclass(frozen=True)
class OrderBookData:
    """A normalized order book snapshot emitted by a streaming provider."""

    exchange: str
    symbol: str
    channel: str
    exchangeTimestamp: float | None
    receiptTimestamp: float
    bids: tuple[tuple[Decimal, Decimal], ...]
    asks: tuple[tuple[Decimal, Decimal], ...]

    @property
    def midPrice(self) -> Decimal | None:
        """Return the midpoint between the best bid and best ask, if available."""
        if not self.bids or not self.asks:
            return None
        return (self.bids[0][0] + self.asks[0][0]) / Decimal(2)

    def print(self, *, console: Console | None = None, maxLevels: int = 10) -> None:
        """Render the latest bid and ask levels as a Rich table."""
        if maxLevels < 1:
            raise ValueError("maxLevels must be at least 1")

        output = console or Console()
        table = Table(title=f"{self.exchange} · {self.symbol} · {self.channel}")
        table.add_column("Side", justify="center")
        table.add_column("Price", justify="right")
        table.add_column("Size", justify="right")

        for price, size in reversed(self.asks[:maxLevels]):
            table.add_row(
                "ASK",
                str(price),
                str(size),
                style="red",
            )
        table.add_row(
            "MID",
            str(self.midPrice) if self.midPrice is not None else "—",
            "best bid / ask",
            style="bold yellow",
        )
        for price, size in self.bids[:maxLevels]:
            table.add_row("BID", str(price), str(size), style="green")
        output.print(table)
