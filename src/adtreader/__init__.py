"""adtreader: open-source reader for Advantage Database Server (.adt) tables."""

from .reader import ADTError, ADTTable, Column, Header, TYPE_NAMES

__all__ = ["ADTError", "ADTTable", "Column", "Header", "TYPE_NAMES"]
__version__ = "0.0.2"
