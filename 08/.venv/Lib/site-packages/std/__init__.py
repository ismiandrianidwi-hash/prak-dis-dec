"""Standard Python utilities and shared integration namespace."""

from importlib.metadata import PackageNotFoundError, version
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

try:
    __version__ = version("standard")
except PackageNotFoundError:
    __version__ = "0+unknown"
