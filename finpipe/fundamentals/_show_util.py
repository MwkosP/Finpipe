"""Internal helpers for stub ``show`` implementations (Rich)."""

from __future__ import annotations
from rich.console import Console


def _show_placeholder(
    module: str,
    ticker: str,
    *,
    hint: str | None = None,
    console: Console | None = None,
) -> None:
    """Print a dim message until the module has a real Rich display."""
    c = console or Console()
    line = f"finpipe.fundamentals.{module}.show — not implemented yet for {ticker!r}."
    if hint:
        line = f"{line} {hint}"
    c.print(f"[dim]{line}[/dim]")
