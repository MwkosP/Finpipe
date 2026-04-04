"""finpipe — technicals and fundamentals over pluggable provider adapters."""

from importlib.metadata import PackageNotFoundError, version

from . import core
from . import derivatives
from . import fundamentals
from . import macro
from . import providers
from . import sentiment
from . import technicals

try:
    __version__ = version("finpipe")
except PackageNotFoundError:
    __version__ = "0.1.0"

__all__ = [
    "__version__",
    "core",
    "derivatives",
    "fundamentals",
    "macro",
    "providers",
    "sentiment",
    "technicals",
]
