"""Pure-Python reader for Advantage Database Server tables (.adt).

The layout implemented here was worked out from sample files. See
docs/FORMAT.md for what is known, what is inferred and what is still open.
"""

from __future__ import annotations

import datetime as _dt
import struct
import uuid
import warnings
from decimal import Decimal
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, Iterator

MAGIC = b"Advantage Table\x00"
HEADER_SIZE = 400
COLUMN_DESCRIPTOR_SIZE = 200
COLUMN_NAME_SIZE = 129  # 128 chars + NUL terminator
RECORD_PREFIX_SIZE = 5  # observed before every record; meaning not yet known

# Julian Day Number of 0001-01-01 (proleptic Gregorian), used to convert
# ADT date values (stored as Julian Day Numbers) to Python dates.
_JDN_OFFSET = 1721425

# Type codes from the ACE API (AdsFieldType enumeration). See docs/FORMAT.md
# for which ones have been verified against real files.
TYPE_NAMES: dict[int, str] = {
    1: "logical",
    2: "numeric",
    3: "date",
    4: "character",
    5: "memo",
    6: "binary",
    7: "image",
    8: "varchar",
    9: "compactdate",
    10: "double",
    11: "integer",
    12: "shortint",
    13: "time",
    14: "timestamp",
    15: "autoinc",
    16: "raw",
    17: "curdouble",
    18: "money",
    19: "int64",
    20: "cicharacter",
    21: "rowversion",
    22: "modtime",
    23: "varchar_fox",
    24: "varbinary_fox",
    25: "system_field",
    26: "nchar",
    27: "nvarchar",
    28: "nmemo",
    29: "guid",
}

# Types whose payload lives in the companion .adm memo file. Not decoded yet.
MEMO_TYPES = {5, 6, 7, 27, 28}

DELETED_FLAG = 0x05  # first byte of the record prefix (from node_adt; inferred)
INT32_NULL = -2**31


class ADTError(Exception):
    """Raised when a file is not a readable ADT table."""


@dataclass(frozen=True)
class Column:
    name: str
    type_code: int
    offset: int  # byte offset inside the record (prefix included)
    length: int

    @property
    def type_name(self) -> str:
        return TYPE_NAMES.get(self.type_code, f"unknown_{self.type_code}")


@dataclass(frozen=True)
class Header:
    record_count: int
    data_offset: int
    record_length: int
    column_count: int


class ADTTable:
    """Read-only view over an .adt file.

    >>> with ADTTable("clientes.adt") as t:
    ...     for row in t:
    ...         print(row)
    """

    def __init__(self, path: str | Path, encoding: str = "cp1252",
                 zero_as_null: bool = True, include_deleted: bool = False) -> None:
        self.path = Path(path)
        self.encoding = encoding
        self.zero_as_null = zero_as_null
        self.include_deleted = include_deleted
        self._fh: BinaryIO = open(self.path, "rb")
        try:
            self.header = self._read_header()
            self.columns = self._read_columns()
        except Exception:
            self._fh.close()
            raise
        self._warned: set[int] = set()

    # -- context manager -------------------------------------------------
    def __enter__(self) -> "ADTTable":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        self._fh.close()

    # -- structure -------------------------------------------------------
    def _read_header(self) -> Header:
        self._fh.seek(0)
        raw = self._fh.read(HEADER_SIZE)
        if len(raw) < HEADER_SIZE:
            raise ADTError("file shorter than the 400-byte header")
        if not raw.startswith(MAGIC):
            raise ADTError("missing 'Advantage Table' signature")
        record_count, data_offset, record_length = struct.unpack_from("<I4xII", raw, 24)
        (column_count,) = struct.unpack_from("<H", raw, 358)
        derived = (data_offset - HEADER_SIZE) // COLUMN_DESCRIPTOR_SIZE
        if column_count != derived:
            warnings.warn(f"column count in header ({column_count}) differs from "
                          f"layout-derived count ({derived}); using derived")
            column_count = derived
        return Header(record_count, data_offset, record_length, column_count)

    def _read_columns(self) -> list[Column]:
        self._fh.seek(HEADER_SIZE)
        cols = []
        for _ in range(self.header.column_count):
            raw = self._fh.read(COLUMN_DESCRIPTOR_SIZE)
            name = raw[:COLUMN_NAME_SIZE].split(b"\x00", 1)[0].decode(self.encoding, "replace")
            type_code, offset, length = struct.unpack_from("<HIH", raw, COLUMN_NAME_SIZE)
            cols.append(Column(name, type_code, offset, length))
        return cols

    # -- records ---------------------------------------------------------
    def __len__(self) -> int:
        return self.header.record_count

    def __iter__(self) -> Iterator[dict[str, Any]]:
        for i in range(self.header.record_count):
            if not self.include_deleted and self.is_deleted(i):
                continue
            yield self.record(i)

    def is_deleted(self, index: int) -> bool:
        return self.raw_record(index)[0] == DELETED_FLAG

    def raw_record(self, index: int) -> bytes:
        if not 0 <= index < self.header.record_count:
            raise IndexError(index)
        self._fh.seek(self.header.data_offset + index * self.header.record_length)
        return self._fh.read(self.header.record_length)

    def record(self, index: int) -> dict[str, Any]:
        raw = self.raw_record(index)
        return {c.name: self._decode(c, raw[c.offset:c.offset + c.length]) for c in self.columns}

    # -- decoding --------------------------------------------------------
    def _decode(self, col: Column, b: bytes) -> Any:
        t = col.type_code
        if self.zero_as_null and not any(b) and t in (1, 3, 4, 13, 14, 20, 22, 26):
            return None
        if t in (4, 20):
            return b.rstrip(b"\x00").decode(self.encoding, "replace").rstrip(" ")
        if t == 26:  # nchar: UTF-16LE, padded
            return b.decode("utf-16-le", "replace").rstrip("\x00").rstrip(" ")
        if t == 1:
            c = b[:1]
            if c in (b"T", b"t", b"Y", b"y"):
                return True
            if c in (b"F", b"f", b"N", b"n"):
                return False
            return None  # observed: b" " (meaning unconfirmed)
        if t == 11:
            v = struct.unpack("<i", b[:4])[0]
            return None if v == INT32_NULL else v
        if t == 15:
            return struct.unpack("<I", b[:4])[0]
        if t == 12:
            return struct.unpack("<h", b[:2])[0]
        if t in (10, 17):
            return struct.unpack("<d", b[:8])[0]
        if t == 18:  # money: int64 with 4 implied decimals
            return Decimal(struct.unpack("<q", b[:8])[0]).scaleb(-4)
        if t in (19, 21):
            return struct.unpack("<q", b[:8])[0]
        if t == 3:
            return _jdn_to_date(struct.unpack("<i", b[:4])[0])
        if t == 13:
            return _ms_to_time(struct.unpack("<i", b[:4])[0])
        if t in (14, 22):
            days, ms = struct.unpack("<ii", b[:8])
            d = _jdn_to_date(days)
            return None if d is None or ms < 0 else _dt.datetime.combine(d, _ms_to_time(ms))
        if t == 29:
            return None if not any(b) else str(uuid.UUID(bytes_le=b[:16]))
        if t not in self._warned:
            self._warned.add(t)
            reason = ("stored in the .adm memo file, not supported yet" if t in MEMO_TYPES
                      else "not decoded yet")
            warnings.warn(f"column type {t} ({TYPE_NAMES.get(t, '?')}) {reason} "
                          f"(e.g. column '{col.name}'); returning raw hex")
        return b.hex()


def _jdn_to_date(n: int) -> _dt.date | None:
    if n <= 0:
        return None
    try:
        return _dt.date.fromordinal(n - _JDN_OFFSET)
    except ValueError:
        return None


def _ms_to_time(ms: int) -> _dt.time:
    s, ms = divmod(ms, 1000)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return _dt.time(h % 24, m, s, ms * 1000)
