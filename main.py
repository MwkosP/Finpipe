"""Run a live order book stream."""

import asyncio

import finpipe as fp


def main() -> None:
    asyncio.run(fp.technicals.streaming.streamOrderBook("BINANCE", "BTC-USDT"))


if __name__ == "__main__":
    main()
