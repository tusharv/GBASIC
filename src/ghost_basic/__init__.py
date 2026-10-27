"""Ghost BASIC: an independently implemented BASIC programming environment."""

from .errors import BasicError
from .program import Program
from .runtime import Runtime

__all__ = ["BasicError", "Program", "Runtime"]
__version__ = "0.3.0"
