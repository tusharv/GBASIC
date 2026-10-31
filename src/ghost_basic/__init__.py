"""Ghost BASIC: an independently implemented BASIC programming environment."""

from .errors import BasicError
from .graphics import Graphics
from .program import Program
from .runtime import Runtime

__all__ = ["BasicError", "Graphics", "Program", "Runtime"]
__version__ = "0.4.1"
