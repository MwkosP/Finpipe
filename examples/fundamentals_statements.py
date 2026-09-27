"""Print SEC financial statements available through EdgarTools.

Run with: ``uv run python examples/fundamentals_statements.py``
"""

from edgar import set_identity
from rich.console import Console

from finpipe.fundamentals import showFinancials


def main() -> None:
    # EdgarTools requires an email identity for SEC fair access.
    set_identity("you@example.com")
    console = Console()

    # These calls fetch and print the statement tables. Income and balance
    # also print headline values when ``headlines=True``.
    showFinancials("NVDA", "income", console=console, headlines=True)
    showFinancials("NVDA", "balance", console=console, headlines=True)
    showFinancials("NVDA", "cashflow", console=console)
    showFinancials("NVDA", "equity", console=console)
    showFinancials("NVDA", "comprehensive", console=console)


if __name__ == "__main__":
    main()
