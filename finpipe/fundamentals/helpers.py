"""Internal helpers shared by fundamentals modules."""

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
    output = console or Console()
    line = f"finpipe.fundamentals.{module}.show — not implemented yet for {ticker!r}."
    if hint:
        line = f"{line} {hint}"
    output.print(f"[dim]{line}[/dim]")
