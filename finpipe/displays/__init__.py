"""Display helpers — Rich formatters (internal; prefer ``fundamentals.financials.*.showXxx``)."""

from .edgar import StatementKind, show_statement

__all__ = [
    "StatementKind",
    "show_statement",
]
