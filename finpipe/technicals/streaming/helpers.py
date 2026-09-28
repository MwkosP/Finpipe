"""Private helpers for technicals streaming APIs."""

from __future__ import annotations

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text

from .objects import OrderBookData


class _OrderBookTerminal:
    """Keep one live terminal view of the latest books per symbol."""

    def __init__(self, exchange: str, symbols: list[str], depth: int | None) -> None:
        self._exchange = exchange
        self._symbols = symbols
        self._depth = depth
        self._books: dict[str, OrderBookData] = {}
        self._live = Live(
            Text(f"Waiting for {exchange} order book data..."),
            console=Console(),
            refresh_per_second=10,
            screen=False,
        )

    def start(self) -> None:
        self._live.start()

    def stop(self) -> None:
        self._live.stop()

    def update(self, book: OrderBookData) -> None:
        previous = self._books.get(book.symbol)
        if previous is not None and previous.bids == book.bids and previous.asks == book.asks:
            return
        self._books[book.symbol] = book
        self._live.update(self._render(), refresh=False)

    def _render(self) -> Table:
        table = Table(title=f"{self._exchange} · Live Order Book", expand=True)
        table.add_column("Market", style="cyan", no_wrap=True)
        table.add_column("Side", justify="center")
        table.add_column("Price", justify="right")
        table.add_column("Size", justify="right")

        for symbol in self._symbols:
            book = self._books.get(symbol)
            if book is None:
                continue
            bids = book.bids if self._depth is None else book.bids[: self._depth]
            asks = book.asks if self._depth is None else book.asks[: self._depth]

            for index, (price, size) in enumerate(reversed(asks), start=1):
                table.add_row(
                    symbol if index == 1 else "",
                    "ASK",
                    str(price),
                    str(size),
                    style="red",
                )

            mid_price = book.midPrice
            table.add_row(
                symbol if not asks else "",
                "MID",
                str(mid_price) if mid_price is not None else "—",
                "best bid / ask",
                style="bold yellow",
            )

            for index, (price, size) in enumerate(bids, start=1):
                table.add_row(
                    symbol if index == 1 and not asks else "",
                    "BID",
                    str(price),
                    str(size),
                    style="green",
                )
            table.add_section()
        return table
