"""Live market data streams backed by optional provider integrations."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping, Sequence
from decimal import Decimal
from typing import Any, Literal

from .helpers import _OrderBookTerminal
from .objects import OrderBookData

BookChannel = Literal["L1_BOOK", "L2_BOOK", "L3_BOOK"]
OrderBookHandler = Callable[[OrderBookData], Awaitable[None] | None]


def _normalize_symbol(symbol: str) -> str:
    normalized = symbol.strip().upper().replace("/", "-")
    if not normalized:
        raise ValueError("symbols must not contain empty values")
    return normalized


def _snapshot_levels(side: Any, depth: int | None) -> tuple[tuple[Decimal, Decimal], ...]:
    count = len(side) if depth is None else min(depth, len(side))
    levels = []
    for index in range(count):
        price, size = side.index(index)
        levels.append((Decimal(str(price)), Decimal(str(size))))
    return tuple(levels)


async def streamOrderBook(
    exchange: str,
    symbols: str | Sequence[str],
    callback: OrderBookHandler | None = None,
    *,
    channel: BookChannel = "L2_BOOK",
    depth: int | None = 20,
    config: Mapping[str, Any] | str | None = None,
) -> None:
    """Run a live crypto order book feed until cancelled or stopped.

    ``exchange`` is any exchange name supported by cryptofeed (for example,
    ``"BINANCE"`` or ``"KRAKEN"``). Symbols use cryptofeed's hyphenated
    notation; CCXT-style ``BTC/USDT`` is also accepted and normalized.
    By default, one live terminal table is updated as snapshots arrive. An
    optional ``callback`` receives each :class:`OrderBookData` snapshot instead;
    it may be regular or async.
    ``depth=None`` includes every level. The feed runs until the surrounding
    task is cancelled; catch ``asyncio.CancelledError`` for graceful shutdown.

    Install the optional integration with ``uv sync --extra streaming``.
    Current cryptofeed releases require Python 3.13 or newer.
    """
    if not isinstance(exchange, str) or not exchange.strip():
        raise ValueError("exchange must be a supported cryptofeed exchange name")
    if channel not in ("L1_BOOK", "L2_BOOK", "L3_BOOK"):
        raise ValueError("channel must be 'L1_BOOK', 'L2_BOOK', or 'L3_BOOK'")
    if depth is not None and (not isinstance(depth, int) or isinstance(depth, bool) or depth < 1):
        raise ValueError("depth must be a positive integer or None")
    if callback is not None and not callable(callback):
        raise TypeError("callback must be callable")

    symbols = [symbols] if isinstance(symbols, str) else list(symbols)
    normalized_symbols = list(dict.fromkeys(_normalize_symbol(symbol) for symbol in symbols))
    if not normalized_symbols:
        raise ValueError("at least one symbol is required")

    try:
        from cryptofeed import FeedHandler
        from cryptofeed.defines import L1_BOOK, L2_BOOK, L3_BOOK
        from cryptofeed.exchanges import EXCHANGE_MAP
    except ImportError as exc:
        raise RuntimeError(
            "Live order book streaming requires cryptofeed. "
            "Install it with `uv sync --extra streaming` on Python 3.13 or newer."
        ) from exc

    exchange_name = exchange.strip().upper()
    if exchange_name not in EXCHANGE_MAP:
        choices = ", ".join(sorted(EXCHANGE_MAP))
        raise ValueError(f"Unsupported cryptofeed exchange {exchange!r}. Supported exchanges: {choices}")

    channel_constant = {"L1_BOOK": L1_BOOK, "L2_BOOK": L2_BOOK, "L3_BOOK": L3_BOOK}[channel]
    terminal = (
        None
        if callback is not None
        else _OrderBookTerminal(exchange_name, normalized_symbols, depth)
    )

    async def on_book(book: Any, receipt_timestamp: float) -> None:
        snapshot = OrderBookData(
            exchange=str(book.exchange),
            symbol=str(book.symbol),
            channel=channel,
            exchangeTimestamp=(float(book.timestamp) if book.timestamp is not None else None),
            receiptTimestamp=float(receipt_timestamp),
            bids=_snapshot_levels(book.book.bids, depth),
            asks=_snapshot_levels(book.book.asks, depth),
        )
        if callback is None:
            terminal.update(snapshot)
        else:
            result = callback(snapshot)
            if inspect.isawaitable(result):
                await result

    handler = FeedHandler(config=config)
    handler.add_feed(
        exchange_name,
        symbols=normalized_symbols,
        channels=[channel_constant],
        callbacks={channel_constant: on_book},
    )
    if terminal is not None:
        terminal.start()
    try:
        await handler.run_async()
    finally:
        if terminal is not None:
            terminal.stop()


__all__ = ["BookChannel", "OrderBookData", "OrderBookHandler", "streamOrderBook"]
