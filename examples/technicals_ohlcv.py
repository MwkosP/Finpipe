"""Fetch and print recent OHLCV bars."""

import finpipe as fp


def main() -> None:
    bars = fp.technicals.fetchOhlcv("NVDA", interval="1d", period="1mo")
    bars.print()

    # The returned object also exposes normalized pandas data and provenance.
    print(bars.toDataFrame().tail())
    print(f"Provider: {bars.provider}; bars: {len(bars)}")
    if bars.fallbackReasons:
        print("Earlier provider failures:")
        for failure in bars.fallbackReasons:
            print(f"  {failure}")

    # Crypto symbols use exchange notation for CCXT. The chain tries CCXT
    # first, with Binance as its default exchange.
    crypto_bars = fp.technicals.fetchOhlcv("BTC/USDT", interval="1d", period="1mo")
    crypto_bars.print()


if __name__ == "__main__":
    main()
