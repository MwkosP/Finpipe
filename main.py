import finpipe as fp

# ______Technicals______
ohlcv = fp.technicals.fetchOhlcv("NVDA", interval="1d", period="1mo")
ohlcv.print()
