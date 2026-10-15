# adt-reader

Open-source, pure-Python reader for **Advantage Database Server** tables (`.adt`). No ADS server, client library or license required.

SAP stopped selling new ADS licenses on 31 August 2025. This project helps people get their data out of ADS tables and into open formats.

> **Status:** early prototype (v0.0.2). The format is being reverse-engineered from data files only. See [docs/FORMAT.md](docs/FORMAT.md) for what is confirmed and what is still open.

## Install (development)

```bash
pip install -e .            # core, no dependencies
pip install -e .[parquet]   # + Parquet export
pip install -e .[dev]       # + pytest
```

## Usage

```bash
adt info clientes.adt
adt export clientes.adt -f csv -o clientes.csv
adt export clientes.adt -f jsonl
adt export clientes.adt -f parquet -o clientes.parquet
adt --encoding cp850 export legacy.adt          # OEM code page tables
```

```python
from adtreader import ADTTable

with ADTTable("clientes.adt") as t:
    print([c.name for c in t.columns])
    for row in t:
        print(row)
```

## Supported column types

| Type | Status |
|---|---|
| character, cicharacter, integer, shortint, autoinc, double, date, logical | ✅ verified against sample files |
| time, timestamp, modtime, money, int64, rowversion, curdouble, nchar, guid | 🟡 decoded per the ACE docs, not yet verified against a real file |
| memo, binary, image, nmemo, nvarchar (stored in `.adm`), numeric, varchar, raw | 🚧 not yet; returned as raw hex with a warning |

Deleted records are skipped by default (`include_deleted=True` to keep them).

## Help wanted: sample files

There are no public sample files for memo/blob (`.adm`), money, timestamp, Unicode and several other types. If you have **ADS or Advantage Data Architect** installed, you can generate a complete synthetic set in about 10 minutes with [`samples/generate_samples.sql`](samples/generate_samples.sql). See [samples/README.md](samples/README.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

This project works only from data files. It does not decompile or redistribute any SAP software.

## License

MIT. Test fixtures come from [ruby-adt](https://github.com/chasemgray/ruby-adt) (MIT); see `NOTICE`.
