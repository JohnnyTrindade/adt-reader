"""Command line interface: `adt info FILE` and `adt export FILE`."""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import sys
from decimal import Decimal

from .reader import ADTTable


def _jsonable(v):
    if isinstance(v, (_dt.date, _dt.time, _dt.datetime)):
        return v.isoformat()
    if isinstance(v, Decimal):
        return str(v)
    return v


def cmd_info(args: argparse.Namespace) -> int:
    with ADTTable(args.file, encoding=args.encoding) as t:
        h = t.header
        print(f"file:          {t.path}")
        print(f"records:       {h.record_count}")
        print(f"record length: {h.record_length} bytes")
        print(f"data offset:   {h.data_offset}")
        print(f"columns:       {h.column_count}\n")
        print(f"{'#':>3}  {'name':<30} {'type':<14} {'offset':>6} {'len':>5}")
        for i, c in enumerate(t.columns):
            print(f"{i:>3}  {c.name:<30} {c.type_name:<14} {c.offset:>6} {c.length:>5}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    with ADTTable(args.file, encoding=args.encoding) as t:
        names = [c.name for c in t.columns]
        out = open(args.output, "w", newline="", encoding="utf-8") if args.output else sys.stdout
        try:
            if args.format == "csv":
                w = csv.writer(out)
                w.writerow(names)
                for row in t:
                    w.writerow(["" if row[n] is None else _jsonable(row[n]) for n in names])
            elif args.format == "jsonl":
                for row in t:
                    out.write(json.dumps({k: _jsonable(v) for k, v in row.items()},
                                         ensure_ascii=False) + "\n")
            elif args.format == "parquet":
                if not args.output:
                    print("parquet export needs -o/--output", file=sys.stderr)
                    return 2
                try:
                    import pyarrow as pa
                    import pyarrow.parquet as pq
                except ImportError:
                    print("parquet export needs pyarrow: pip install adtreader[parquet]",
                          file=sys.stderr)
                    return 2
                out.close()
                rows = list(t)
                table = pa.Table.from_pylist(rows)
                pq.write_table(table, args.output)
        finally:
            if args.output and not out.closed:
                out.close()
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="adt", description="Read Advantage Database (.adt) tables")
    p.add_argument("--encoding", default="cp1252",
                   help="text encoding for character columns (default cp1252; try cp850 for OEM tables)")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("info", help="show header and column layout")
    pi.add_argument("file")
    pi.set_defaults(func=cmd_info)

    pe = sub.add_parser("export", help="export records")
    pe.add_argument("file")
    pe.add_argument("-f", "--format", choices=["csv", "jsonl", "parquet"], default="csv")
    pe.add_argument("-o", "--output", help="output file (default: stdout)")
    pe.set_defaults(func=cmd_export)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
